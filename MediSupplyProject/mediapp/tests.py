from django.test import TestCase, Client
from django.urls import reverse
from .models import User, PurchaseOrder, OrderItem


class MediSupplyFlowTests(TestCase):
    def setUp(self):
        # Create users
        self.staff = User.objects.create_user(username='staff1', password='password', role='staff')
        self.manager = User.objects.create_user(username='mgr1', password='password', role='manager')
        self.supplier = User.objects.create_user(username='sup1', password='password', role='supplier')

        # Create a pending order by staff
        self.order = PurchaseOrder.objects.create(created_by=self.staff)

        self.client = Client()

    def test_add_order_items(self):
        # Staff logs in
        self.client.login(username='staff1', password='password')

        # Prepare formset POST data
        url = reverse('add_order_items', args=[self.order.order_id])
        data = {
            'order_items-TOTAL_FORMS': '1',
            'order_items-INITIAL_FORMS': '0',
            'order_items-MIN_NUM_FORMS': '0',
            'order_items-MAX_NUM_FORMS': '1000',
            'order_items-0-description': 'Gauze pads',
            'order_items-0-quantity': '10',
            'order_items-0-price': '1.50',
            'order_items-0-DELETE': '',  # required because can_delete=True
        }

        # Post and follow redirect back to order list
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check the database got the item
        from .models import OrderItem
        items = OrderItem.objects.filter(purchase_order=self.order, description='Gauze pads')
        self.assertEqual(items.count(), 1)

        # Total should be 10 * 1.50 = 15.00
        self.order.refresh_from_db()
        self.assertEqual(float(self.order.total_amount), 15.00)

        # Ensure the updated total appears in the orders list
        self.assertContains(response, "15.00")



    def test_order_list_visibility(self):
        # Create additional orders with different statuses
        po2 = PurchaseOrder.objects.create(created_by=self.staff, status='Approved')
        po3 = PurchaseOrder.objects.create(created_by=self.staff, status='Pending')

        # Staff sees all their orders
        self.client.login(username='staff1', password='password')
        resp = self.client.get(reverse('order_list'))
        # Look specifically for the <td> ORDER_ID </td> cells
        self.assertContains(resp, f"<td>{self.order.order_id}</td>")
        self.assertContains(resp, f"<td>{po2.order_id}</td>")
        self.assertContains(resp, f"<td>{po3.order_id}</td>")

        # Manager sees only Pending orders (1 and 3)
        self.client.login(username='mgr1', password='password')
        resp = self.client.get(reverse('order_list'))
        self.assertContains(resp, f"<td>{self.order.order_id}</td>")
        self.assertContains(resp, f"<td>{po3.order_id}</td>")
        self.assertNotContains(resp, f"<td>{po2.order_id}</td>")

        # Supplier sees only Approved orders (2)
        self.client.login(username='sup1', password='password')
        resp = self.client.get(reverse('order_list'))
        self.assertContains(resp, f"<td>{po2.order_id}</td>")
        self.assertNotContains(resp, f"<td>{self.order.order_id}</td>")
        self.assertNotContains(resp, f"<td>{po3.order_id}</td>")



    def test_approve_and_reject_order(self):
        # Manager approves the order
        self.client.login(username='mgr1', password='password')
        url = reverse('approve_order', args=[self.order.order_id])
        resp = self.client.post(url, {'action': 'approve'}, follow=True)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Approved')

        # Reset status and test rejection
        self.order.status = 'Pending';
        self.order.save()
        resp = self.client.post(url, {'action': 'reject'}, follow=True)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Rejected')

    def test_supplier_update_status(self):
        # First approve the order so supplier can update
        self.order.status = 'Approved'
        self.order.save()

        self.client.login(username='sup1', password='password')
        url = reverse('supplier_update', args=[self.order.order_id])

        # Update to Shipped
        resp = self.client.post(url, {'status': 'Shipped'}, follow=True)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Shipped')

        # Update to Delivered
        resp = self.client.post(url, {'status': 'Delivered'}, follow=True)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Delivered')


