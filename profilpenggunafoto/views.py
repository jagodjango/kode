from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def profil_pengguna(request, username):
    user = get_object_or_404(klass=User, username=username)  # otomatis menampilkan HTTP 404 jika username tidak ada

    # menyiapkan template, untuk menyederhanakan, menggunakan string, belum menggunakan template dari file
    t = Template("Halo {{ pengguna }}<br/>{% if pengguna.profil %}{{ pengguna.profil.nomorponsel }}{% endif %}")
    c = Context({'pengguna': user})

    return HttpResponse(t.render(context=c))
