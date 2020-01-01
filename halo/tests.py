from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class HaloTest(TestCase):

    def test_halo_index(self):
        response = self.client.get(reverse('halo-index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('UTF-8'), 'halo Django')  # content is in bytes string
