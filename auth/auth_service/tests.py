from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class AuthServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_register_view(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'Account Created for newuser'
        })

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_signin_view(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'User Logged in Successfully'
        })

        response = self.client.post(url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_signout_view(self):
        url = reverse('logout')
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'Logged out Successfully'
        })

        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_changepassword_view(self):
        url = reverse('changepassword')
        
    
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': "User is not Logged In please log in"
        })

        
        self.client.login(username='testuser', password='testpassword123')
        

        data = {
            'old_password': 'testpassword123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'Password Changed Successfully'
        })

       
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'Invalid Method'
        })

        data = {
            'old_password': 'wrongoldpassword',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())