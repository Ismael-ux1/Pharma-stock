from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.pk is not None:  # if order exists
            orig = Order.objects.get(pk=self.pk)
            if orig.status != 'delivered' and self.status == 'delivered':  # if status changed to 'delivered'
                Sale.objects.create(product=self.product, buyer=self.created_by, quantity=self.quantity, price=self.price)  # create a sale
        super().save(*args, **kwargs)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.price * self.quantity

