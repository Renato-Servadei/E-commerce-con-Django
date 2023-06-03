from carts.models import Cart
from django.db import models
from enum import Enum
from users.models import User


class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAID = 'PAID'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

choices = [ (tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices = choices, default='CREATED')
    shipping_total = models.DecimalField(max_digits=8, decimal_places=2, default=5)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''