from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created_at')

admin.site.register(Cart, CartAdmin)
# Register your models here.
