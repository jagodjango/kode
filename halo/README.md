# Django App halo dunia! (hello world)

### Langkah untuk integrasikan dengan Django Project 

* tambahkan direktori `halo` ke sebuah Django Project
* tambahkan `HaloConfig` ke settings
```
INSTALLED_APPS = [
    'halo.apps.HaloConfig',
    # apps lain
]
```
* tambahkan `halo/` ke urls di Django Project
```
urlpatterns = [
    # paths lain
    path('halo/', include('halo.urls')),
]
```
* (opsional) jika ingin membuat halaman utama dipindahkan ke `/halo/` lakukan
```
from django.views.generic.base import RedirectView

urlpatterns = [
    # paths lain
    path('', RedirectView.as_view(url='/halo/', permanent=False)),
    path('halo/', include('halo.urls')),
]
```

### Isi dari Django App `halo`

* dibandingkan sebuah Django App yang baru dibuat, bedanya `halo` menambahkan satu file `urls.py`,
file ini akan diacu oleh `urls.py` yang ada di Django Project untuk URL yang diawali **/halo/**

* di file `urls.py`, dengan menuliskan path string kosong (''), artinya halaman utama **/halo/**,
akan diarahkan untuk diproses ke views dengan nama (fungsi) index. Kemudian path ini diberi nama **halo-index**,
untuk dapat dikenali di seluruh proyek dengan nama tersebut, contohnya ada di bagian tests.

* Django App `halo` dilengkapi dengan pengujian `tests.py`, yang akan mengakses halaman dengan nama `halo-index`,
melalui fungsi `reverse()`, nama `halo-index` akan diubah menghasilkan URL **/halo/**.

* Pengujian pertama pada `test_halo_index()` adalah memastikan halamannya dapat diakses atau HTTP 200,
jadi halamannya tidak hilang (misalnya HTTP 404) atau tidak mengalami error server (misalnya HTTP 5xx).

* Pengujian kedua pada `test_halo_index()` adalah memastikan isi dari halamannya sesuai dengan definisi awal,
yakni berisi sebuah text 'halo Django', jadi bukan berisi halaman lain atau teks lainnya.

##### Selamat datang di Jago Django! Membahas berbagai fitur framework Django untuk pemrograman Web dengan Python.
