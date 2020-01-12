from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nomorponsel = models.CharField(max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return 'Profil #{} untuk User #{}'.format(self.id, self.user.id)
