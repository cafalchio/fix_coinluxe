from django import forms


class AddCreditsForm(forms.Form):
    product_price = forms.DecimalField(label='Credits')
    
class BuyCryptoForm(forms.Form):
    crypto_id = forms.IntegerField(widget=forms.HiddenInput())
    amount = forms.FloatField(label='Amount')