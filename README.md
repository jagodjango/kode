![](https://github.com/oonid/jagodjango/workflows/Django%20apps/badge.svg)
[![codecov](https://codecov.io/gh/oonid/jagodjango/branch/master/graph/badge.svg)](https://codecov.io/gh/oonid/jagodjango)

# Jago Django

> ya, itu berima.

## Tentang

_Repository_ ini berisi kode-kode penggunaan fitur (hingga tingkat lanjut) dari framework Django untuk pemrograman web
dengan Python, dibahas dalam Bahasa Indonesia.

### Menggunakan Kodenya

Setelah `clone` _repository_ ini, masukkan direktori yang diperlukan ke Django Project,
setiap direktori adalah satu Django _App_.

### Aplikasi Django yang Tersedia
* [halo](halo/README.md): aplikasi `hello world` yang dilengkapi dengan `tests`.
* [splitviewsmodels](splitviewsmodels/README.md): aplikasi dengan file `views.py` atau/dan `models.py` diubah menjadi 
direktori (_python package_), dengan meminimalisir perubahan dalam proses `import` (jika melakukan _refactor_).
Dilengkapi dengan `tests` untuk `views` dan `models`.
* [profilpenggunafoto](profilpenggunafoto/README.md): aplikasi yang menambahkan field `nomorponsel` dan `foto` ke
sistem autentikasi dan autorisasi bawaan di Django `contrib.auth.models.User`. Dilengkapi dengan `test` untuk `views` dan `models`
(termasuk `ImageField` dengan pengujian upload gambar).

### Versi Kompatibel

Proses `test` dilakukan untuk Python 3.6, 3.7, 3.8 dan Django 2.2 LTS, 3.0.

Pengecekan dengan GitHub Actions [workflow Django apps](https://github.com/oonid/jagodjango/actions?query=workflow%3A%22Django+apps%22), keberhasilannya ditampilkan pada badge di atas.

## Catatan

* Masih diperlukan menambahkan cara kontribusi, biasanya file **CONTRIBUTING**.md.
* Gunakan fitur [isu](https://github.com/oonid/jagodjango/issues) untuk diskusi atau memberikan masukan.

## Kontributor

* **oon arfiandwi** [@oonid](https://github.com/oonid)
