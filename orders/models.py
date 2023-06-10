from carts.models import Cart
from django.db import models
from django.db.models.signals import pre_save
from enum import Enum
from shipping_addresses.models import ShippingAddress
from users.models import User
import uuid

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

choices = [ (tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices = choices, default='CREATED')
    shipping_total = models.DecimalField(max_digits=8, decimal_places=2, default=5)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id
    
    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address
        
        shipping_address = self.user.shipping_address
        if shipping_address:
            self.update_shipping_address(shipping_address)
            
        return shipping_address
    
    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()
    
    def get_total(self):
        return self.cart.total + self.shipping_total
    
def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)