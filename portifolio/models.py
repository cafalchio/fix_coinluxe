# from django.db import models
# from django.contrib.auth.models import User
# from api_backend.models import CryptoCurrency


# class Holding(models.Model):
#     portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
#     cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
#     amount = models.FloatField(null=True)


# class Portfolio(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     holdings = models.ManyToManyField(CryptoCurrency, through=Holding)
