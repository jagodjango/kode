# Django App Split Views Models (File jadi Direktori)

### Objektif

Mengubah file `views.py` atau/dan `models.py` menjadi direktori 
(_python package_ `views`, `models`), sehingga  bisa dipisahkan 
menjadi beberapa file, ini lebih baik dibandingkan hanya satu file 
yang terlalu panjang.

Hasil pengubahan sebisa mungkin tidak banyak mengubah mekanisme `import`, 
karena untuk proyek yang sudah besar, proses _refactor_ yang memengaruhi 
mekanisme `import` akan lebih panjang (sulit) prosesnya.

### Langkah untuk integrasikan dengan Django Project

* tambahkan direktori `splitviewsmodels/` ke sebuah Django Project
* tambahkan `SplitviewsmodelsConfig` ke **settings.py**
```
INSTALLED_APPS = [
    'splitviewsmodels.apps.SplitviewsmodelConfig',
    # apps lain
]
```
* tambahkan `split/` ke **urls.py** di direktori Django Project
```
from django.urls import path, include  # tambahkan fungsi include

urlpatterns = [
    # paths lain
    path('split/', include('splitviewsmodels.urls')),
]
```
* lakukan persiapan pembuatan tabel dari model `TabelA` dan `TabelB` dengan perintah 
`python manage.py makemigrations splitviewsmodels` dan pastikan tidak ada error.
Proses ini akan menghasilkan file baru di direktori `migrations/`, misalnya file `0001_initial.py` 
yang berisi skenario pembuatan tabel-tabel tersebut.
* lakukan proses migrasi untuk pemasangan tabel-tabel tersebut ke basis data dengan perintah 
`python manage.py migrate splitviewsmodels` dan pastikan lagi tidak ada error.
* cek kembali apakah skenario sudah terpasang dengan perintah 
`python manage.py showmigrations splitviewsmodels` atau bisa juga tanpa penyebutan nama Django App 
`python manage.py showmigrations` akan menampilkan semua Django App yang terinstal.

### Isi dari Django App `splitviewsmodels`

* dibandingkan sebuah Django App yang baru dibuat, bedanya `splitviewsmodels` menambahkan satu file `urls.py`,
file ini akan diacu oleh `urls.py` yang ada di Django Project untuk URL yang diawali **/split/**

* di file `urls.py`, dengan menuliskan _path_ `'fa'`, maka _path_ lengkapnya adalah **/split/fa** dimana akan diproses 
ke `views` dengan nama (fungsi) `fitur_a`. Terlihat di sini, tidak ada perbedaan dalam melakukan `import` dari `views`, 
tidak ada penyebutan nama modul `fa` (file `fa.py`). Berikutnya _path_ ini diberi nama `fitur-a`, untuk dapat
dikenali di seluruh proyek dengan nama tersebut, contohnya ada di bagian `tests`.

* di file `urls.py`, untuk penulisan _path_ `'fb'` penjelasannya mirip dengan penulisan _path_ `'fa'` di atas. 
Tidak ada perbedaan dalam melakukan `import` dari `views`, tidak ada penyebutan nama modul `fb` (file `fb.py`).

* **fokus utama** dari Django App ini memberikan contoh menggantikan file `views.py` dengan sebuah _python package_ 
`views`, yaitu sebuah direktori `views` yang di dalamnya berisi file `__init__.py`. Secara bawaan, pada saat Django App 
dibuat ada file `views.py`, kemudian file ini dapat dihapus jika sudah dibuat _package_ `views`. Dalam direktori 
inilah, kita dapat membuat sejumlah file python baru, misalnya kita pisahkan satu fitur masuk dalam satu file, agar 
setiap file isinya tidak terlalu panjang. **fokus berikutnya** memastikan proses `import` tidak berubah seperti pada
saat hanya satu file, dengan mendaftarkan semua file dan fitur di dalamnya ke `__init__.py` yang ada dalam _package_ 
`views` tersebut.
```
from .fa import *  # impor semua fungsi di file fa sebagai fungsi dari views
from .fb import *  # impor semua fungsi di file fb sebagai fungsi dari views
```

* **fokus utama** selanjutnya adalah memberikan contoh menggantikan file `models.py` dengan sebuah _python package_ 
`models`, yaitu sebuah direktori `views` yang di dalamnya berisi file `__init__.py`. Mekanismenya sama dengan
sebelumnya, dimana file `models.py` bawaan dari pembuatan Django App dapat dihapus jika sudah dibuat _package_
`models`.  Mengenai **fokus berikutnya** dimana proses `import` tidak berubah, kita juga daftarkan ke `__init__.py`.
```
from .ta import *  # impor semua model (tabel) and fungsi di file ta sebagai definisi dari models
from .tb import *  # impor semua model (tabel) and fungsi di file ta sebagai definisi dari models
```

* Django App `splitviewsmodels` dilengkapi dengan `tests.py`, yang akan mengakses halaman yang terdefinisi di 
`urls.py`, serta menguji model basis data yang terkait.

* Pada `test_fitur_a` akan menguji melalui akses halaman dengan nama `'fitur-a'` yang dikonversi melalui fungsi 
`reverse()` menghasilkan path URL **/split/fa** untuk dipastikan dapat diakses atau HTTP 200. Kemudian isi dari
halamannya dicek sesuai dengan kembalian views (fungsi) `fitur_a`.

* Pada `test_fitur_b` akan menguji mirip dengan skenario sebelumnya, bedanya dalam views (fungsi) `fitur_b_1` melakukan
_query_ ke dua model (tabel di basis data). Sehingga saat dipastikan halamannya dapat diakses atau HTTP 200, artinya
juga memastikan bahwa koneksi ke basis data juga berhasil. **Catatan**: bahwa dalam proses pengujian akan membuat
basis data baru, sehingga terpisah dari basis data yang digunakan saaat dioperasikan, dan dimulai dari kosong.

* Pada `test_tabel` akan menguji lebih detail model (tabel di basis data). Menguji dengan melakukan _query_ dari model,
menguji dengan memastikan masih kosong, mengisi dari model (dan field) yang sesuai, kemudian menguji bahwa proses 
mengisi data berhasil.

### Untuk Mengoperasikan

Dari direktori Django Project, eksekusi perintah: `python manage.py runserver`.
Kemudian buka URL `http://127.0.0.1:8000/split/fa` dan `http://127.0.0.1:8000/split/fb`
 di browser. 
 
Untuk berhenti dari proses `runserver`, dengan menekan `Ctrl c`.

### Untuk Menguji

Dari direktori Django Project, eksekusi perintah: `python manage.py test splitviewsmodels`

##### Selamat datang di Jago Django! Membahas berbagai fitur framework Django untuk pemrograman Web dengan Python.
