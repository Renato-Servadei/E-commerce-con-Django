from django.db import models
from products.models import Product

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    product = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
