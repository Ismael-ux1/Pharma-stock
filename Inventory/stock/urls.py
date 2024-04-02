from django.urls import path
from . import views
from .views import sales_report

urlpatterns = [
    path("dash/", views.index, name="dash"),
    path('products/', views.products, name='products'),
    path("orders/", views.orders, name="orders"),
    path('sales_report/', sales_report, name='sales_report'),
    path('users/', views.users, name='users'),
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),
]
