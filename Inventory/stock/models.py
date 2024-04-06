from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
import uuid
from django.core.exceptions import ValidationError


class Category(models.Model):
    """ Category model definition """
    name = models.CharField(max_length=100)  # name field
    description = models.TextField(blank=True, null=True)  # description field

    def __str__(self):
        # String representation of the catagory model
        return self.name


class Product(models.Model):
    """ product model definition """
    name = models.CharField(max_length=100, unique=True)  # product name field
    # Foreign key to category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # product description field
    description = models.TextField(blank=True, null=True)
    # product price field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # product quantity field
    quantity = models.PositiveIntegerField(null=True)

    serial_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    # time stamp for when the product was created
    created_at = models.DateTimeField(auto_now_add=True)
    # time stamp for the last update of the product
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # string representation of the product model
        return self.name


class UserProfile(models.Model):
    """ UserProfile model defination """
    # one-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    # User's physical address field
    physical_address = models.CharField(max_length=40, null=True)
    # User's mobile number field
    mobile = models.CharField(max_length=12, null=True)
    # User's profile picture field
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        # string representation of the userprofile model
        return self.user.username


class Order(models.Model):
    """ order model definition """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    # Foreign key to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Foreign key to the User model
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    # quantity of the product ordered
    quantity = models.IntegerField()
    # price of the product ordered
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # status of the order
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='Pending')

    # time stamp when the order was created
    created_at = models.DateTimeField(auto_now_add=True)
    # time stamp of the last update of the order
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        # property to calculate the total price of the order
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.pk is not None:  # if order exists
            orig = Order.objects.get(pk=self.pk)
            if orig.status != 'Delivered' and self.status == 'Delivered':  # if status changed to 'delivered'
                Sale.objects.create(product=self.product, buyer=self.created_by, quantity=self.quantity, price=self.price)  # create a sale
                # Decrease the product quantity
                self.product.quantity -= self.quantity
                self.product.save()
        super().save(*args, **kwargs)


class Sale(models.Model):
    """ sale model definition """

    # Foreign key to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Foreign key to the User model
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    # Quantity of the product sold
    quantity = models.IntegerField()
    # Price of the product sold
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # tmestamp for when the sale was made
    created_at = models.DateTimeField(auto_now_add=True)
    # tmestamp for the last update of the sale
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        # Property to calculate the total price of the sale
        return self.price * self.quantity
