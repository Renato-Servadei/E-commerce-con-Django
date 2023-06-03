from django.db import models
from django.db.models.signals import pre_save, m2m_changed, post_save
from products.models import Product
from users.models import User
import uuid
import decimal

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
        
    FEE = 0.05

    def __str__(self):
        return self.cart_id
    
    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        order = self.order_set.first()
        if order:
            order.update_total()


    def update_subtotal(self):
        # self.subtotal = sum([products.price for products in self.products.all()])
        # self.save()

        # actualizamos el calculo del subtotal multiplicando la cantidad de cada producto por el precio
        self.subtotal = sum([
            cp.quantity * cp.product.price for cp in self.products_related()
        ]) 
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    def products_related(self):
        return self.cartproducts_set.select_related('product')

class CartProductsManager(models.Manager):
    #con esta clase obtnemos o creamos un objeto cart. si ya esta creado se actualiza la cantida del product
    def create_or_update_quantity(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:
            quantity = object.quantity + quantity
        object.update_quantity(quantity)    
        return object

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    #lo traemos de cartProductsManager para actualizar la cantidad de producto
    objects = CartProductsManager()

    def update_quantity(self, quantity = 1):
        self.quantity = quantity
        self.save()

def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id= str(uuid.uuid4())

def update_totals(instance, sender, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_totals(instance, sender, *args, **kwargs):
        instance.cart.update_totals()

pre_save.connect(set_cart_id, sender=Cart)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(update_totals, sender=Cart.products.through)

