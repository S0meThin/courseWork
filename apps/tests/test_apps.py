from django.test import TestCase, Client
from django.urls import reverse
from apps.models import itemList, orders, itemOrdered, transactions, returns, Store

class TestViews(TestCase):

    def test_call_view_deny_anonymous(self):
        response = self.client.get('/dest/article_lookup', follow=True)
        self.assertRedirects(response, '/login/')
        response = self.client.post('/dest/manual_order', follow=True)
        self.assertRedirects(response, '/login/')