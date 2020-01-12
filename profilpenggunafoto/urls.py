from django.urls import path

from profilpenggunafoto import views

app_name = 'profil'
urlpatterns = [
    path('<str:username>/', views.profil_pengguna, name='pengguna'),
]
