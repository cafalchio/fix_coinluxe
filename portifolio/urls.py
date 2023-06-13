from django.urls import path
from .views import add_credits, get_credits, payment_cancelled, payment_successful, stripe_webhook

urlpatterns = [
    path("get-credits/", get_credits, name="get_credits"),
    path("add_credits/", add_credits, name="add_credits"),
    path("payment_successful/", payment_successful, name="payment_successful"),
    path("payment_cancelled/", payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook/", stripe_webhook, name="stripe_webhook"),
]
