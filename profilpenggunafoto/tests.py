from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile

from hashlib import sha1


from .models import Profil
from .views import profil_pengguna


class ProfilTest(TestCase):
    _root_username = 'root'             # contoh username
    _root_password = 't00r'             # contoh password
    _root_email = 'root@localhost'      # contoh email
    _root_nomorponsel = '081234567890'  # contoh nomorponsel
    _halaman_profil = reverse('profil:pengguna', kwargs={'username': _root_username})            # namespace 'profil'
    _halaman_profil_tidak_ada = reverse('profil:pengguna', kwargs={'username': _root_password})  # namespace 'profil'
    _small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )  # contoh gambar gif yang akan digunakan untuk foto profil, 37 bytes

    def setUp(self) -> None:
        # setUp dengan mengisi data di basis data (untuk setiap test, akan memanggil setUp secara independen)

        # isi data di tabel
        self._root = User.objects.create_superuser(username=self._root_username, email=self._root_email,
                                                   password=self._root_password)
        self._root_profil = Profil.objects.create(user=self._root, nomorponsel=self._root_nomorponsel, )

    def test_tabel(self):
        self.assertTrue(isinstance(self._root, User))
        self.assertTrue(isinstance(self._root_profil, Profil))
        self.assertTrue(isinstance(self._root.profil, Profil))     # test OneToOneField
        self.assertTrue(isinstance(self._root_profil.user, User))  # test OneToOneField

    def test_akses_proxy(self):
        # test untuk method __str__() dari Profil
        self.assertEqual(str(self._root_profil), 'Profil #{} untuk User #{}'
                         .format(self._root_profil.id, self._root.id))

        # test akses profil dari User melalui model Profil, memberikan contoh cara akses profil dari User
        self.assertEqual(self._root.profil, self._root_profil)

    def test_query(self):
        # test query profil and check nomorponsel
        _u = User.objects.filter(username=self._root_username).first()  # sudah pasti setUp mengisi data 'root'
        self.assertEqual(_u, self._root)
        # test nomorponsel, memberikan contoh cara akses nomorponsel dari User melalui proxy profil
        self.assertEqual(_u.profil.nomorponsel, self._root_nomorponsel)

        # test query User berdasarkan nomorponsel
        self.assertTrue(User.objects.filter(profil__nomorponsel=self._root_nomorponsel).exists())  # root user exists

    def test_views_dengan_request(self):
        # melakukan simulasi memanggil views langsung, sehingga butuh membuat Request menggunakan RequestFactory

        # https://docs.djangoproject.com/en/dev/topics/testing/advanced/#the-request-factory
        # set request factory to access views
        self.factory = RequestFactory()

        # membuat objek request dengan akses ke halaman profil-pengguna untuk username root
        request = self.factory.get(self._halaman_profil)

        # mencoba mengakses tanpa login, jadi menggunakan AnonymousUser()
        request.user = AnonymousUser()
        self.assertTrue(request.user.is_anonymous)

        # membuat response dari mengirimkan request ke views
        response = profil_pengguna(request, username=self._root_username)
        self.assertEqual(response.status_code, 302)  # HTTP 302 Found redirect, dikirim ke halaman login

        # mencoba mengakses menggunakan user root yang sebelumnya dibuat
        # request.user ini membutuhkan AuthenticationMiddleware
        request.user = self._root
        self.assertTrue(request.user.is_authenticated)

        # membuat response dari mengirimkan request ke views
        response = profil_pengguna(request, username=self._root_username)
        self.assertEqual(response.status_code, 200)  # HTTP 200 OK, berhasil akses halaman profil root

    def test_views_tanpa_login(self):
        # melakukan simulasi memanggil views melalui HTTP client

        # membuat response dengan mengakses menggunakan HTTP client (tanpa login, default AnonymousUser)
        response = self.client.get(self._halaman_profil)
        self.assertEqual(response.status_code, 302)  # HTTP 302 Found redirect, dikirim ke halaman login

        # HTTP client dilengkapi dengan fitur untuk follow redirect, dicontohkan berikut ini
        # halaman login bawaan django, dengan LoginView dan templates menggunakan bawaan django.contrib.admin
        # path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
        response = self.client.get(self._halaman_profil, follow=True)
        self.assertEqual(response.status_code, 200)  # HTTP 200 OK, berhasil akses halaman accounts/login/

    def test_views_dengan_login(self):
        # melakukan simulasi memanggil views melalu HTTP client yang menggunakan login() atau force_login()

        # melakukan autentikasi dengan login()
        logged_in = self.client.login(username=self._root_username, password=self._root_password)
        self.assertTrue(logged_in)  # berhasil login

        # melakukan autentikasi yang salah dengan login()
        logged_in = self.client.login(username=self._root_username, password=self._root_username)
        self.assertFalse(logged_in)  # gagal login

        # memaksakan autentikasi dengan force_login() dengan user root yang sudah dibuat pada test setUp
        self.client.force_login(user=self._root)
        self.assertEqual(get_user(self.client), self._root)  # cek login sesuai
        self.assertEqual(int(self.client.session['_auth_user_id']), self._root.id)  # cek session sudah login (alt)

        # membuat response dengan mengakses menggunakan HTTP client (sudah login)
        response = self.client.get(self._halaman_profil)
        self.assertEqual(response.status_code, 200)  # HTTP OK, berhasil akses halaman_profil

        # mengecek halaman profil isinya sesuai yang login, konten dalam string bytes, ubah dgn decode()
        self.assertEqual(response.content.decode('UTF-8'),
                         'Halo {}<br/>{}'.format(self._root.username, self._root.profil.nomorponsel))

        # membuat response dengan mengakses menggunakan HTTP client (sudah login), tapi halamannya tidak ada
        response = self.client.get(self._halaman_profil_tidak_ada)
        self.assertEqual(response.status_code, 404)  # HTTP 404 Not Found

    def test_profil_foto_upload(self):
        # test upload
        self._root_profil.foto = SimpleUploadedFile('small.gif', self._small_gif, content_type='image/gif')
        self._root_profil.save()  # save foto

        # pastikan ukuran dari hasil upload sama
        self.assertEqual(self._root_profil.foto.size, len(self._small_gif))

        hash_gif = sha1(self._small_gif)
        hash_foto = sha1()
        with self._root_profil.foto.open('rb') as f:
            if f.multiple_chunks():
                for chunk in f.chunks():
                    hash_foto.update(chunk)
            else:
                hash_foto.update(f.read())
        # pastikan hasil upload dan gambar asli memiliki hash sha1 yang sama
        self.assertEqual(hash_gif.hexdigest(), hash_foto.hexdigest())
