from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)
        context['message']= 'Listado de Productos' 
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name  = 'products/product.html'
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        return context

