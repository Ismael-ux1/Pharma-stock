from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from stock.models import Product, Order
from .models import Product, Order


class UserRegistry(UserCreationForm):

    # Defines an email field in addition to default fields
    email = forms.EmailField()

    class Meta:
        # Specifies the model to be used for the form
        model = User
        fields = [  # Defines the fields to be included in the form
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        # Specifies the model to be used for the form
        model = Product

        # Defines the fields to be included in the form
        fields = ["name", "category", "quantity",  "price", "description"]


class OrderForm(forms.ModelForm):
    class Meta:
        # Specifies the model to be used for the form
        model = Order
        fields = [  # Defines the fields to be included in the form
            'product', 'created_by', 'quantity', 'price', 'status'
        ]
        widgets = {
            # Customizes the widget for 'product' field
            'product': forms.Select(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}), }
