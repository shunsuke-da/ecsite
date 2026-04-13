from django.contrib import admin

# Register your models here.
from .models import Items, Carts, CartItems

admin.site.register(Items)

admin.site.register(Carts)
admin.site.register(CartItems)