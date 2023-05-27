from django.db.models.query import Q
from django.views.generic import ListView, DetailView
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
    

class ProductSearchListView(ListView):
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        filters = Q(title__icontains = self.query()) | Q(category__title__icontains = self.query())
        return Product.objects.filter(filters).distinct() #agregué distinct para evitar que me devuelva dos veces el mismo producto
    
    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)
        context['query']= self.query() 
        context['count']= context['products'].count()
        return context
