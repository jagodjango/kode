from django.test import TestCase
from django.urls import reverse
from django.db import models

from .models import TabelA, TabelB

# Create your tests here.


class FiturATest(TestCase):

    def test_fitur_a(self):
        response = self.client.get(reverse('fitur-a'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('UTF-8'), 'Fitur A')  # konten dalam string bytes, ubah dgn decode()


class FiturBTest(TestCase):

    def test_fitur_b(self):
        response = self.client.get(reverse('fitur-b-1'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('UTF-8'), 'Fitur B #1')  # konten dalam string bytes, ubah dgn decode()

    def test_tabel(self):
        # test dengan tabel kosong
        qa = TabelA.objects.all()  # simulasikan query yang dilakukan di fitur_b_1
        qb = TabelB.objects.all()  # simulasikan query yang dilakukan di fitur_b_1
        self.assertTrue(isinstance(qa, models.query.QuerySet))
        self.assertTrue(isinstance(qb, models.query.QuerySet))
        self.assertEqual(0, qa.count())  # pastikan tabel memang awalnya masih kosong
        self.assertEqual(0, qb.count())  # pastikan tabel memang awalnya masih kosong

        # isi data di tabel
        na = TabelA.objects.create(nama='AA')  # sesuai definisi model, isi dengan field (kolom) nama
        nb = TabelB.objects.create(nama='BB')  # sesuai definisi model, isi dengan field (kolom) nama
        self.assertTrue(isinstance(na, TabelA))
        self.assertTrue(isinstance(nb, TabelB))

        # test dengan tabel isi
        qa = TabelA.objects.all()  # simulasikan query yang dilakukan di fitur_b_1
        qb = TabelB.objects.all()  # simulasikan query yang dilakukan di fitur_b_1
        self.assertEqual(1, qa.count())  # cek jumlah sesuai yang diisikan di tabel
        self.assertEqual(1, qb.count())  # cek jumlah sesuai yang diisikan di tabel
