from django.contrib import admin
from .models import Customer, Cart, OrderPlaced, Product, Category, ProductImage


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'zipcode', 'state']


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_name']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'offer', 'discounted_price',
                    'description', 'brand', 'category_name', 'product_image']
    readonly_fields = ('discounted_price',)
    inlines = [ProductImageAdmin]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'product', 'quantity', 'ordered_date', 'status']
