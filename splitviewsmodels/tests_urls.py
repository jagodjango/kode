from django.urls import path, include

urlpatterns = [
    path('split/', include('splitviewsmodels.urls')),
]
