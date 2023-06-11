from django import template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Credits

register = template.Library()

@login_required
@register.simple_tag
def get_credits(request):
    user = request.user
    credits = Credits.objects.filter(user=user).first()
    return credits.amount if credits else 0.00