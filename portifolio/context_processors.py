from portifolio.models import Credits

def credits(request):
    if request.user.is_authenticated:
        credits = Credits.objects.filter(user=request.user).first()
        if credits is None:
            credits = "0.00"
        return {'credits': credits}
    else:
        return {'credits': "0.00"}