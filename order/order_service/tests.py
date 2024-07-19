from django.test import TestCase, Client
from django.urls import reverse
from order_service.models import Order, OrderedItem
from decimal import Decimal
import json
from unittest.mock import patch
from django.contrib.auth.models import User

@patch('django.contrib.auth.models.User.is_authenticated', return_value=True)
class OrderServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.order = Order.objects.create(ordered_by=self.user.username)
        self.item = OrderedItem.objects.create(
            order=self.order,
            product_id="test_product",
            quantity=2,
            price=Decimal('10.00')
        )

    def test_get_orders(self, mock_auth):
        url = reverse('get_orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json())
        self.assertIn('total_pages', response.json())
        self.assertIn('current_page', response.json())

    def test_get_order_detail(self, mock_auth):
        url = reverse('get_order_detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.order.id)
        self.assertIn('items', response.json())

    def test_get_order_total(self, mock_auth):
        url = reverse('get_order_total', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['order_id'], self.order.id)
        self.assertIn('total_price', response.json())
        self.assertIn('item_count', response.json())

    def test_update_order_item(self, mock_auth):
        url = reverse('update_order_item', args=[self.item.id])
        data = {
            'product_id': 'updated_product',
            'quantity': 3,
            'status': 'SHIPPED'
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Item updated Successfully', response.json()['message'])

    def test_non_existent_order(self, mock_auth):
        url = reverse('get_order_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_non_existent_item(self, mock_auth):
        url = reverse('update_order_item', args=[9999])
        data = {'quantity': 5}
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)