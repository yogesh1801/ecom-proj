from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from product_manage.models import Product
from product_manage import views
import json

class ProductManageTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            category='electronics',
            stock=10,
            price=100,
            created_by=self.user.username
        )

    def test_create_product(self):
        url = reverse('create_product')
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'category': 'books',
            'stock': 5,
            'price': 50
        }
        request = self.factory.post(url, data)
        request.user = self.user
        response = views.create(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('product created with id', json.loads(response.content)['message'])

    def test_edit_product(self):
        url = reverse('edit_product', args=[self.product.id])
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
            'category': 'clothing',
            'stock': 15,
            'price': 150
        }
        request = self.factory.post(url, data)
        request.user = self.user
        response = views.edit(request, self.product.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['message'], "Product details updated successfully.")

    def test_product_details(self):
        url = reverse('product_details', args=[self.product.id])
        request = self.factory.get(url)
        response = views.details(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['name'], 'Test Product')

    def test_user_products(self):
        url = reverse('user_products', args=[1])
        request = self.factory.get(url)
        request.user = self.user
        response = views.user_products(request, 1)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('products', content)
        self.assertIn('page', content)

    def test_all_products(self):
        url = reverse('all_products', args=[1])
        request = self.factory.get(url)
        response = views.all_products(request, 1)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('products', content)
        self.assertIn('page', content)

    def test_delete_product(self):
        url = reverse('delete_product', args=[self.product.id])
        request = self.factory.post(url)
        request.user = self.user
        response = views.delete_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], "Product Deleted Successfully")

    def test_product_status(self):
        url = reverse('product_status', args=[self.product.id])
        request = self.factory.post(url)
        request.user = self.user
        response = views.product_status(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Active status Successfully set to', json.loads(response.content)['message'])

    def test_get_price(self):
        url = reverse('get_price', args=[self.product.id])
        request = self.factory.get(url)
        response = views.get_price(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['price'], '100')