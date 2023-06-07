from .models import Order

def get_or_create_order(cart, request):

    order = cart.order

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(user = request.user, cart = cart)
    
    if order:
        request.session['order_id'] = order.order_id

    return order