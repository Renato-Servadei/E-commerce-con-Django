from carts.utils import get_or_create_cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order
from .utils import get_or_create_order

@login_required(login_url='login')
def order(request):

    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    
    return render(request, 'orders/order.html', {'order': order, 'cart': cart})