from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistry, ProductForm, OrderForm
from django.views.generic import ListView, CreateView
from .models import Product, Order, Sale
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
import pandas as pd
import json
from django.db.models import F, Sum


@login_required  # Decorator to ensure the user is authenticated
def index(request):
    """ view function for the index page """
    # get all the users
    users = User.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()
    reg_users = len(User.objects.all())
    sales = Sale.objects.all()

    order_count = orders.count()
    product_count = len(products)
    sale_count = sales.count()

    # check if the HTTP request method is POST
    if request.method == 'POST':
        # Initialize the OrderForm with data from the POST request
        form = OrderForm(request.POST)
        # validate the form data
        if form.is_valid():
            # save the form data to a new Order object,
            # but don't commit to the database yet
            obj = form.save(commit=False)
            # Set the customer of the Order to the current user
            obj.customer = request.user
            # Save the Order object to the database
            obj.save()
            # # Redirect the user to the dashboard index page
            return redirect('dashboard-index')
    else:
        # Initialize an empty OrderForm
        form = OrderForm()

    context = {  # Define the context data for the template
        'tittle': "Home",
        'users': users,
        'form': form,
        'orders': orders,
        'products': products,
        'sales': sales,
        'order_count': order_count,
        'product_count': product_count,
        'sale_count': sale_count,
        "count_users": reg_users,
    }
    # Render the 'stock/index.html' template with the context data
    return render(request, 'stock/index.html', context)


@login_required
def products(request):
    """ view function for handling products """

    # query all products from the database
    products = Product.objects.all()
    # chech if the form is valid
    if request.method == "POST":
        # create a from instance and populate it with data from the request
        form = ProductForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # save the form data to the database
            form.save()
            # Redirect to the product page
            return redirect("products")
    # create a new form instance
    else:
        form = ProductForm()

    # Context data to be passed to the template
    context = {"title": "Products", "products": products, "form": form}
    # Render the template with the context data
    return render(request, "stock/products.html", context)


@login_required(login_url='login')
def orders(request):
    orders = Order.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Check if the quantity ordered is more than,
            # the quantity available in the product
            if instance.quantity > instance.product.quantity:
                messages.error(request, 'The quantity ordered cannot be more than the quantity available in the product.')
            # Check if the price matches the actual product price
            elif instance.price != instance.product.price:
                messages.error(request, 'The price does not match the actual product price.')
            else:
                instance.created_by = request.user
                instance.save()
                messages.success(request, 'Order created successfully.')
                return redirect("orders")
    else:
        form = OrderForm()
    context = {"title": "Orders", "orders": orders, "form": form}
    return render(request, "stock/orders.html", context)


@login_required
def sales_report(request):
    # Get all sales
    sales = Sale.objects.all()
    # Calculate total sales
    total_sales = sales.aggregate(total=Sum(F('price') * F('quantity')))['total']

    # Calculate sales per product
    sales_per_product = sales.values('product__name').annotate(total=Sum(F('price') * F('quantity')))

    # Calculate sales per buyer
    sales_per_buyer = sales.values('buyer__username').annotate(total=Sum(F('price') * F('quantity')))

    context = {
        'total_sales': total_sales,
        'sales_per_product': sales_per_product,
        'sales_per_buyer': sales_per_buyer,
    }

    return render(request, 'stock/sales_report.html', context)

@login_required
def users(request):
    users = User.objects.all()
    context = {"title": "Users", "users": users}
    return render(request, "stock/users.html", context)


@login_required
def user(request):
    context = {"profile": "User Profile"}
    return render(request, "stock/user.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistry()
    context = {"register": "Register", "form": form}
    return render(request, "stock/register.html", context)
