from django.shortcuts import render
from .models import Carts
def cart(request):
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Carts.objects.get(pk = cart_id)        
    else:
        cart = Carts.objects.create(user=user)
    request.session['cart_id'] = cart.id

    return render(request, 'carts/cart.html', {})
