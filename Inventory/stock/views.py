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
import plotly.express as px
from plotly.offline import plot
import json


@login_required
def index(request):
    users = User.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()
    sales = Sale.objects.all()
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

    order_count = orders.count()
    product_count = len(products)
    sale_count = sales.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()

    context = {
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
    return render(request, 'stock/index.html', context)


@login_required
def products(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()
    context = {"title": "Products", "products": products, "form": form}
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
    context = {
    'sales': sales,
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
