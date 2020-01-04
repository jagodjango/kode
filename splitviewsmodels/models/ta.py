from django.db import models


class TabelA(models.Model):
    nama = models.CharField(max_length=10, null=True, blank=True)
