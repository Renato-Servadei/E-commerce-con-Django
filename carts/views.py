from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartProducts
from .utils import get_or_create_cart


def cart(request):
    
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {'cart': cart})

def add(request):

    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))

    # cart.products.add(product, through_defaults={
    #     'quantity': quantity
    # })
    #implementamos otra forma de crear la relacion entre carrito y productos
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)
    #al hacerlo así se crea un nuevo item en el carrito (o sea que si agregamos más cantidad de un producto que
    # ya estaba en el carrito lo vamos a ver dos veces, por eso seguimos modificando el archivo .models creando
    # la clase CartProductManager)
    return render(request, 'carts/add.html', {
        'product': product,
        'cart_product' : cart_product,
        'quantity': quantity,
        })

def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')