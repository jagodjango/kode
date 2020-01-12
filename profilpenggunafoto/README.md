# Django App Profil Pengguna (dengan tambahan field) Foto

### Objektif

Menunjukkan cara membuat halaman wajib login khas Django, menggunakan cukup _decorator_ **@login_required** [^1], 
**tanpa perlu** _sesions_ (secara manual) atau mekanisme lain.

Menunjukkan penambahan `field` **nomorponsel** dan **foto** di Profil yang merupakan _proxy_ ke tabel User.
Salah satu mekanismenya adalah membuat satu model (misalnya kita beri nama) Profil, lalu kita buat relasi model ini 
**one-to-one** ke model User. Bisa juga diakses menggunakan panel Django Admin.

Untuk mekanisme yang lain, baca lebih detail di bagian **Isi dari Django App**.

Menunjukkan sejumlah skenario `test`:
* Pengujian dengan `setUp` di awal, yang bisa diakses (secara independen) oleh sejumlah `tests` berikutnya.
* Pengujian memasukkan ke basis data, menguji relasi one-to-one, menguji akses profil sebagai proxy dari `User`,
melakukan query ke basis data.
* Pengujian `views` dengan `AnonymousUser` (tanpa login) yang otomatis dipindahkan ke halaman login,
pengujian dengan login `User memastikan autentikasi berhasil.
* Pengujian dengan HTTP Client maupun menggunakan RequestFactory.

Dengan menggunakan `settings` yang minimum, memberikan pengetahuan tentang apa yang dibutuhkan untuk autentikasi:
* INSTALLED_APPS: 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
* AUTHENTICATION_BACKENDS (sudah ada nilai default)
* MIDDLEWARE: 'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',

### Langkah untuk integrasikan dengan Django Project

* instalasi paket `Pillow` menggunakan `pip` untuk menggunakan ImageField di Django.
```
pip install Pillow
```
* tambahkan direktori `profilpenggunafoto/` ke sebuah Django Project
* tambahkan `ProfilpenggunafotoConfig` ke **settings.py**
```
INSTALLED_APPS = [
    'profilpenggunafoto.apps.ProfilpenggunafotoConfig',
    # apps lain
]
```
* (jika belum ada) tambahkan `MEDIA_URL` dan `MEDIA_ROOT` ke **settings.py**, untuk `ImageField`.
```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
* terkait `MEDIA_ROOT`, Anda perlu menambahkan direktori `media` di dalam direktori Django Project, sejajar dengan
direktori-direktori Django Apps. Di dalam direktori `media` ditambahkan juga direktori `images` untuk upload foto dari
`ImageField` yang ada di Model Profil. Di beberapa kondisi, misalnya di lingkungan development, direktori `media/images`
ini akan dibuat secara otomatis pada saat Anda upload gambar ke Django Admin, tapi untuk menjamin bahwa direktori
tersebut ada dan tidak menyebabkan error saat dioperasikan.
Misalnya perintah berikut dieksekusi di direktori Django Project.
```
mkdir media
cd media
mkdir images
```
* lakukan persiapan pembuatan tabel dari model `Profil` dengan perintah 
`python manage.py makemigrations profilpenggunafoto` dan pastikan tidak ada error.
Proses ini akan menghasilkan file baru di direktori `migrations/`, misalnya file `0001_initial.py` 
yang berisi skenario pembuatan tabel-tabel tersebut.
* lakukan proses migrasi untuk pemasangan tabel-tabel tersebut ke basis data dengan perintah 
`python manage.py migrate profilpenggunafoto` dan pastikan lagi tidak ada error.
* cek kembali apakah skenario sudah terpasang dengan perintah 
`python manage.py showmigrations profilpenggunafoto` atau bisa juga tanpa penyebutan nama Django App 
`python manage.py showmigrations` akan menampilkan semua Django App yang terinstal.
* untuk menggunakan halaman panel Django Admin, jangan lupa tambahkan akun superuser sebelum bisa login di halaman tsb.
```
python manage.py createsuperuser
```

### Isi dari Django App `profilpenggunafoto`

Django secara bawaan sudah menyediakan User dan Group, lengkap dengan mekanisme autentikasi dan autorisasi [^2].
Jika dilihat di dokumentasi tersebut, `User` di Django sudah memiliki field:

* username
* password
* email
* first_name
* last_name

Lalu bagaimana kalo kita membutuhkan tambahan field? misalnya yang paling sering digunakan zaman sekarang adalah 
nomor HP dan juga foto profil.

Ada 3 cara [^3] untuk menambahkan field, mulai dari yang paling sederhana, sampai mengubah keseluruhan mekanisme 
autentikasi. 

1. Mekanisme proxy ke model User, ini yang paling sederhana, tanpa mengubah autentikasi.
2. Mekanisme untuk menggantikan model User, dengan mewarisi (extends) class AbstractUser.
3. Dan yang paling mendasar sekali perubahannya adalah dengan mewarisi (extends) class AbstractBaseUser.

Di sini kita akan **fokus** pada cara yang paling sederhana dahulu (1).

* dibandingkan sebuah Django App yang baru dibuat, bedanya `profilpenggunafoto` menambahkan satu file `urls.py`,
file ini akan diacu oleh `urls.py` yang ada di Django Project menggunakan `namespace` **profil** untuk URL yang diawali 
**/profil/** kemudian `username`, `<str:username>` artinya variabel `username` dengan tipe str (string), 
akan dikirimkan ke fungsi `profil_pengguna`.

* **fokus utama** dari Django App ini memberikan contoh pada `models.py` ditambahkan model Profil,
dengan relasi **one-to-one** ke model User, sebagai proxy untuk mengakses `nomorponsel` dan `foto`.

* menggunakan panel Django Admin untuk menampilkan Profil yang terhubung ke model User, dengan mengubah 
file `admin.py`. Ini akan memudahkan Anda untuk memastikan bahwa Profil sudah terhubung ke User, kemudian
upload untuk foto pengguna sudah pada direktori yang sesuai.

* Django App ini dilengkapi dengan `tests.py` yang akan menguji semua yang dijelaskan di bagian Objektif, pengujian
dilakukan pada `views` untuk memastikan semua fungsi webnya diuji, maupun `models` untuk memastikan semua data yang
disimpan maupun dicari dari basis data sesuai. Diawali dengan bagian `setUp`, sebagian paling awal yang akan digunakan
oleh semua tests secara idenpenden.

* Pada `test_tabel` diuji mengenai instance dari `User` dan `Profil` serta relasi `OneToOneField` antara keduanya.

* Pada `test_akses_proxy` memastikan bahwa relasi `User` dan `Profil` sudah dapat digunakan untuk mengakses proxy,
dimana artinya kebutuhan untuk penambahan field pada `User` sudah terpenuhi.

* Pada `test_query` diuji untuk pencarian data (query) baik dari sisi `User` maupun dari sisi `Profil`, dengan
menggunakan relasi yang dimiliki.

* Pada `test_views_dengan_request` fokus pada pengujian fungsi `profil_pengguna`, dimana salah satu parameternya adalah
`Request`, sehingga pada pengujian ini akan menggunakan `RequestFactory`. Skenario pengujian tanpa login menggunakan
`AnonymousUser`, sedangkan pengujian dengan login menggunakan pengguna yang dibuat pada `setUp`.

* Pada `test_views_tanpa_login` menggunakan HTTP Client untuk menguji views, sehingga akan menggunakan URL dari halaman
profil, menggunakan nama `views` dan `namespace` yang sesuai. Pengujian khusus skenario tanpa login, untuk menunjukkan
bahwa halaman yang wajib login akan otomatis `redirect` ke halaman login, jika pengguna belum login. Untuk memastikan
halaman login sampai terbuka, maka menggunakan fitur `follow=True` dari HTTP Client. Untuk kebutuhan ini kita
menggunakan `templates` halaman login dari `django.contrib.admin`, dapat dilihat di file `urls.py` dalam potongan kode
`LoginView.as_view(template_name='admin/login.html')`.

* Pada `test_views_dengan_login` dengan fokus skenario login, menggunakan sejumlah teknik login dari HTTP Client.
Kemudian dilakukan pengujian hingga halaman profil untuk pengguna dapat terbuka, diverifikasi dengan tampilan yang
muncul sesuai dengan `views` dengan data pengguna yang login. Terdapat juga pengujian untuk membuka halaman profil
yang tidak ada.

* Di bagian `test_profil_foto_upload` yakni test yang terakhir, memastikan bahwa field `foto` yang ada pada `Profil`
yang berjenis `ImageField`, dapat menerima _upload_ gambar, kemudian setelah dilakukan proses _upload_ diuji bahwa
file sumber sama dengan file yang sudah tersimpan sebagai foto profil pengguna.

### Untuk Mengoperasikan

Dari direktori Django Project, eksekusi perintah: `python manage.py runserver`.
Kemudian buka `http://127.0.0.1/admin` di browser untuk mengakses halaman panel Django Admin.

Untuk berhenti dari proses `runserver`, dengan menekan `Ctrl c`.

### Untuk Menguji

Dari direktori Django Project, eksekusi perintah: `python manage.py test profilpenggunafoto`

### Apabila terjadi Error

* Misalnya Anda mendapatkan pesan kesalahan tentang paket `Pillow` seperti di bawah ini, artinya dalam sistem 
(virtual environment) yang Anda gunakan belum terpasang (terinstal) `Pillow`, baca kembali bagian integrasi di atas.
```
$ python manage.py makemigrations
SystemCheckError: System check identified some issues:

ERRORS:
profilpenggunafoto.Profil.foto: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "pip install Pillow".
```

* Misalnya Anda tidak dapat login ke halaman Django Admin, pastikan akun yang Anda gunakan merupakan akun superuser 
(atau akun yang punya atribut staf).

### Pranala
[^1]: https://docs.djangoproject.com/en/dev/topics/auth/default/#the-login-required-decorator
[^2]: https://docs.djangoproject.com/en/dev/topics/auth/
[^3]: https://docs.djangoproject.com/en/dev/topics/auth/customizing/

##### Selamat datang di Jago Django! Membahas berbagai fitur framework Django untuk pemrograman Web dengan Python.
