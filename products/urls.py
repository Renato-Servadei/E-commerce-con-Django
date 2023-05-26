from django.urls import path
from .views import ProductDetailView, ProductSearchListView 

urlpatterns = [
    
    path('search', ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product')
]