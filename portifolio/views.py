from collections import UserDict
import time
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import stripe
from .models import Credits, UserPayment

register = template.Library()


@login_required
def get_credits(request):
    user = request.user
    credits = Credits.objects.filter(user=user).first()
    return credits.amount if credits else 0.00


# https://www.youtube.com/watch?v=hZYWtK2k1P8&t=222s


@login_required(login_url="login")
def add_credits(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
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
            + "/payment_succesful?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "portifolio/add_credits.html")


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.user_id
    user_payment = UserPayment.objects.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, "portifolio/payment_successful.html", {"customer": customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, "portifolio/payment_cancelled.html")

def save_credits(user, amount):
    user_obj = UserDict.objects.get(username=user)
    credits, _ = Credits.objects.get_or_create(user=user_obj)
    credits.amount += amount
    print("save credits")
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
        session_id = session.get("id", None)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        item = line_items.data[0]
        credits = item.price.unit_amount / 100
        print(f"\n_____________________________________Credits -> {credits}\n")
        save_credits(user=request.user, credits = credits)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)


    
# def use_credits(user, amount):
#     user_obj = UserDict.objects.get(username=user)
#     credits, created = Credits.objects.get_or_create(user=user_obj)
#     credits.amount -= amount
#     credits.save()
    
