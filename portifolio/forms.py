from django import forms


class AddCreditsForm(forms.Form):
    product_price = forms.DecimalField(label='Credits')
    
class BuyCryptoForm(forms.Form):
    amount = forms.DecimalField()