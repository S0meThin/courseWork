from django.test import TestCase, Client
from django.urls import reverse
from login.models import Users

class TestView(TestCase):

    def test_login_GET(self):
        client = Client()
        response = client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'Login.html')