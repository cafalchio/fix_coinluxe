from django import forms


class AddCreditsForm(forms.Form):
    product_price = forms.DecimalField(label='Credits')
    

class BuyCryptoForm(forms.Form):
    ammount = forms.DecimalField(label='Ammount')