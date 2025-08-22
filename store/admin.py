from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'created')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('available',)
    search_fields = ('name', 'description')
