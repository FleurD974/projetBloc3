from django.test import TestCase
from django.urls import reverse

from accounts.models import Customer


class LoggedInTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            email="usertest@test.com",
            first_name="User",
            last_name="Test",
            password="test123"
        )
        
    def test_invalid_login(self):
        data = {'email': 'usertest@test.com', 'password': 'test'}
        response = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        
    def test_profile_change(self):
        self.client.login(email="usertest@test.com",
                            password="test123")
        
        data = {
            "email": "usertest@test.com",
            "password": "test123",
            "first_name": "User",
            "phone_number": "01020304",
            "last_name": "User"
        }
        response = self.client.post(reverse('accounts:profile'), data=data)
        self.assertEqual(response.status_code, 302)
        user_test = Customer.objects.get(email="usertest@test.com")
        self.assertEqual(user_test.last_name, "User")
