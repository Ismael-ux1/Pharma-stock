from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("/", include("stock.urls")),
    path('admin/', admin.site.urls),    
    path(
        "", auth.LoginView.as_view(template_name="stock/login.html"), name="login"
    ),
    path(
        "logout/",
        auth.LogoutView.as_view(template_name="stock/logout.html"),
        name="logout",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
