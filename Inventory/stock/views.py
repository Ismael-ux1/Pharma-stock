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
import pandas as pd
import json


@login_required  # Decorator to ensure the user is authenticated
def index(request):
    """ view function for the index page """

    # get all the users
    users = User.objects.all()
    # get all orders
    orders = Order.objects.all()
    # get all products
    products = Product.objects.all()
    # get all sales
    sales = Sale.objects.all()
    # get the  count of all users
    reg_users = len(User.objects.all())

    # Check each order
    for order in orders:
        # If the order is delivered and a corresponding Sale does not exist
        if order.status == 'Delivered' and not Sale.objects.filter(order=order).exists():
            # Create a new Sale
            Sale.objects.create(
                product=order.product,
                buyer=order.buyer,
                quantity=order.quantity,
                price=order.price
            )

    # Update the sales list after potentially creating new Sales
    sales = Sale.objects.all()

    # get the count of all orders
    order_count = orders.count()
    # get the count of all products
    product_count = len(products)
    # get the count of all sales
    sale_count = sales.count()

    # if the request methos is POST
    if request.method == 'POST':
        # Instantiate the OrderForm with the POST data
        form = OrderForm(request.POST)
        # if the form is valid
        if form.is_valid():
            # save the form but dont commit to the database yet
            obj = form.save(commit=False)
            # set the customer to the current user
            obj.customer = request.user
            # save the form to the database
            obj.save()
            # redirect the dashboard index
            return redirect('dashboard-index')
    # if the request method is not POST
    else:
        # Instatiate an empty OrderForm
        form = OrderForm()

    context = {  # context dictionary to pass to the template
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
    # Render the index page with the context
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
    print([i for i in request])
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect("orders")
    else:
        form = OrderForm()
    context = {"title": "Orders", "orders": orders, "form": form}
    return render(request, "stock/orders.html", context)


@login_required
def sales_view(request):
    sales = Sale.objects.all()  # Get all sales
    context = {'sales': sales, }
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
