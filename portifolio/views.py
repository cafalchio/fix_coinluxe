import time
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
import stripe

from models import CryptoCurrency
from .models import Credits, Holding, Portfolio

register = template.Library()


@login_required
def get_credits(request):
    user = request.user
    credits = Credits.objects.filter(user=user).first()
    return credits.amount if credits else 0.00


# https://www.youtube.com/watch?v=hZYWtK2k1P8&t=222s


@login_required(login_url="account_login")
def add_credits(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    metadata = {"user_id": str(request.user.id)} 
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": settings.PRODUCT_PRICE,
                    "quantity": 1,
                },
            ],
            mode="payment",
            customer_creation="always",
            success_url=settings.REDIRECT_DOMAIN
            + "/payment_successful?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
            metadata=metadata, 
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "portifolio/add_credits.html")


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    if settings.DEBUG:
        print(f"{session} -> Session ID")
        print(f"{customer} -> costumer ")
    return render(request, "portifolio/payment_successful.html", {"customer": customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, "portifolio/payment_cancelled.html")

def save_credits(user, amount):
    print("Save credits")
    print(f"user {user}, amount: {amount}")
    credits, created = Credits.objects.get_or_create(user=user)
    if created:
        credits.amount = amount
    else:
        credits.amount += amount
    credits.save()
    
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(8)
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")
        user = User.objects.get(id=user_id) if user_id else None
        session_id = session.get("id", None)
        time.sleep(4)    
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        item = line_items.data[0]
        credits = int(item.amount_total) / 100
        save_credits(user=user, amount=credits)
    return HttpResponse(status=200)


@login_required(login_url="account_login")
def buy_crypto(request):
    user = request.user
    crypto_id = request.POST.get('crypto_id')
    amount = request.POST.get('amount')
    portfolio, _ = Portfolio.objects.get_or_create(owner=user)
    crypto = get_object_or_404(CryptoCurrency, id=crypto_id)
    holding, _ = Holding.objects.get_or_create(portfolio=portfolio, cryptocurrency=crypto)
    holding.amount += float(amount)
    holding.save()
    return render(request, 'buy_crypto.html')

