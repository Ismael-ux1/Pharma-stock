from django.contrib import admin
from .models import Category, Product, UserProfile, Order, Sale

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ("name", "description")

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "serial_number", "description", "price", "quantity", "created_at", "updated_at")
    list_filter = ["category"]
    search_fields = ["name"]

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("user", "physical_address", "mobile", "picture")
    list_filter = ["user"]
    search_fields = ["user"]

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("product", "created_by", "quantity", "price", "status", "created_at", "updated_at")
    list_filter = ["created_at"]
    search_fields = ["product"]

class SaleAdmin(admin.ModelAdmin):
    model = Sale
    list_display = ("product", "buyer", "quantity", "price", "created_at", "updated_at")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sale, SaleAdmin)
