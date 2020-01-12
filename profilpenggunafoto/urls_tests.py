from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # pinjam admin/login.html dari modul contrib.admin
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
    path('profil/', include('profilpenggunafoto.urls', namespace='profil')),
]
