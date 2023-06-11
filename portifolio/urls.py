from django.urls import path
from .views import get_credits

urlpatterns = [
    path('get-credits/', get_credits, name='get_credits'),
]