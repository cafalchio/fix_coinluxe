from django.urls import reverse_lazy
from django.views.generic.edit import (DeleteView,
                                       UpdateView, 
                                       CreateView)
from django.views.generic import ListView, DetailView, View
from .models import Product


class ProductBaseView(View):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('Products:all')


class ProductListView(ProductBaseView, ListView):
    """View to list all Products.
    Use the 'Product_list' variable in the template
    to access all Product objects"""

class ProductDetailView(ProductBaseView, DetailView):
    """View to list the details from one Product.
    Use the 'Product' variable in the template to access
    the specific Product here and in the Views below"""

class ProductCreateView(ProductBaseView, CreateView):
    """View to create a new Product"""

class ProductUpdateView(ProductBaseView, UpdateView):
    """View to update a Product"""

class ProductDeleteView(ProductBaseView, DeleteView):
    """Delete a Product"""