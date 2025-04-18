from django.test import TestCase, Client
from django.urls import reverse
from .models import User, PurchaseOrder


class PurchaseOrderTests(TestCase):
    def setUp(self):
        # a Hospital Staff user
        self.staff = User.objects.create_user(username='user1', password='password', role='staff')
        # a Purchasing Manager
        self.manager = User.objects.create_user(username='manager1', password='password', role='manager')
        self.client = Client()

    def test_create_purchase_order(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('create_order'), {

            'status': 'Pending'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(PurchaseOrder.objects.filter(created_by=self.staff).exists())

