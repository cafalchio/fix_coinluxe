from django import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Credits

register = template.Library()

@login_required
def get_credits(request):
    user = request.user
    credits = Credits.objects.filter(user=user).first()
    return credits.amount if credits else 0.00

@login_required
def add_credits(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        user = request.user
        credits = Credits.objects.filter(user=user).first()

        if credits is None:
            credits = Credits.objects.create(user=user, amount=int(amount))
        else:
            credits.amount += int(amount)
            credits.save()
    return render(request, 'portifolio/add_credits.html')