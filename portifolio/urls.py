from django.urls import path
from .views import add_credits, get_credits

urlpatterns = [
    path('get-credits/', get_credits, name='get_credits'),
    path('add_credits/', add_credits, name='add_credits')
]