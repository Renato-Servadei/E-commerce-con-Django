from carts.utils import get_or_create_cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from shipping_addresses.models import ShippingAddress
from .models import Order
from .utils import get_or_create_order, breadcrumb

@login_required(login_url='login')
def order(request):

    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    
    return render(request, 'orders/order.html', 
                  {'order': order, 
                   'cart': cart,
                   'breadcrumb': breadcrumb()})

@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingaddress_set.count() > 1

    return render(request, 'orders/address.html', {
        'order': order,
        'cart': cart,
        'breadcrumb': breadcrumb(address=True),
        'shipping_address': shipping_address,
        'can_choose_address': can_choose_address
    })

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })

@login_required(login_url='login')
def check_address(request, pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user.id:
        return redirect('index')
    
    order.update_shipping_address(shipping_address)
    return redirect('orders:address')