from django.contrib import admin
from .models import Category, Item, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity']
    list_filter = ['user', 'item']
    search_fields = ['user__username', 'item__name']
