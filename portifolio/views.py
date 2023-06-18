import time
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import stripe
from decimal import Decimal
from api_backend.models import CryptoCurrency
from portifolio.forms import BuyCryptoForm, SellCryptoForm
from .models import Credits, Holding, Portfolio
import logging
logging.basicConfig(level=logging.INFO)

@login_required
def get_credits(request):
    user = request.user
    credits = Credits.objects.filter(user=user).first()
    return credits.amount if credits else 0.00


# https://www.youtube.com/watch?v=hZYWtK2k1P8&t=222s


@login_required(login_url="login")
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

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(6)
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
        user = User.objects.get(id=user_id)
        logging.info(f"User - {user}")
        session_id = session.get("id", None)
        time.sleep(8)    
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        logging.info(f"line_items - {line_items}")
        item = line_items.data[0]
        logging.info(f"item - {item}")
        value = int(item.amount_total) / 100
        logging.info(f"amount - {value}")
        credits, _ = Credits.objects.get_or_create(user=user)
        logging.info(f"Credits amount - {credits.amount}")
        credits.amount += Decimal(value)
        logging.info(f"credits.amount - {credits.amount}")
        credits.save()
    return HttpResponse(status=200)


@login_required(login_url="account_login")
def buy_crypto(request, pk):
    user = request.user
    credit, _ = Credits.objects.get_or_create(user=user)
    crypto = get_object_or_404(CryptoCurrency, id=pk)
    if request.method == 'POST':
        form = BuyCryptoForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            price = crypto.current_price * float(amount)  # total price
            portfolio, _ = Portfolio.objects.get_or_create(owner=user)
            holding, created = Holding.objects.get_or_create(portfolio=portfolio, cryptocurrency=crypto)
            if not holding.amount:
                holding.amount = 0
            if created:
                holding.amount = float(amount)
            else:
                holding.amount += float(amount)
            holding.save()
            
            credit.amount -= Decimal(price)
            credit.save()
            
            return redirect('portfolio')
        
    else:
        form = BuyCryptoForm()

    return render(request, 'portifolio/buy_crypto.html', {'form': form, 'crypto': crypto, 'credit': credit})

@login_required(login_url="account_login")
def sell_crypto(request, pk):
    user = request.user
    credit, _ = Credits.objects.get_or_create(user=user)
    crypto = get_object_or_404(CryptoCurrency, id=pk)
    if request.method == 'POST':
        form = SellCryptoForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            price = crypto.current_price * float(amount)  # total price
            portfolio, _ = Portfolio.objects.get_or_create(owner=user)
            holding, _ = Holding.objects.get_or_create(portfolio=portfolio, cryptocurrency=crypto)
            if holding.amount - float(amount) >=0:
                holding.amount -= float(amount)
            else:
                form = SellCryptoForm()
            holding.save()
            
            credit.amount += Decimal(price) - (Decimal(price)/100) * 2
            credit.save()
            
            return redirect('portifolio')
        
    else:
        form = SellCryptoForm()

    return render(request, 'portifolio/sell_crypto.html', {'form': form, 'crypto': crypto, 'credit': credit})



@login_required(login_url="account_login")
def portfolio_view(request):
    template_name = "portifolio/portifolio.html"
    user = request.user
    try:
        portfolio = Portfolio.objects.get(owner=user)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(owner=user)
    if portfolio:
        holdings = Holding.objects.filter(portfolio=portfolio)
        crypto_data = []
        for holding in holdings:
            value_eur = f"{holding.amount * holding.cryptocurrency.current_price:.2f} €"
            crypto_data.append({
                'crypto': holding.cryptocurrency,
                'amount': holding.amount,
                'f_amount': holding.formatted_amount,
                'value' : value_eur,
            })
    else:
        crypto_data = []
    
    context = {'crypto_data': crypto_data}
    return render(request, template_name, context)


    