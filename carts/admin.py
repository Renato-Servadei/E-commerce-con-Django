from django.contrib import admin
from .models import Carts

class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')

admin.site.register(Carts)
# Register your models here.
