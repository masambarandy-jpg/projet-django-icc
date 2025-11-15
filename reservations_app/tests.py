from django.test import TestCase
from django.urls import reverse

class ReservationTests(TestCase):
    def test_homepage_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
