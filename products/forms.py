from django import forms
from stripe import Product


class ProductForm(forms.ModelForm):
    # Customizations for the form fields or behavior can be added here

    class Meta:
        model = Product
        fields = '__all__'