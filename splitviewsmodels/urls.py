from django.urls import path

from splitviewsmodels import views

urlpatterns = [
    path('fa', views.fitur_a, name='fitur-a'),
    path('fb', views.fitur_b_1, name='fitur-b-1'),
]
