from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_customer_registration_success(self):
        """Test successful customer registration"""
        response = self.client.post(reverse('customer_register'), {
            'username': 'testcustomer',
            'email': 'customer@test.com',
            'date_of_birth': '1990-01-01',
            'password': 'testpass123',
            'password_confirmation': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='testcustomer', user_type='customer').exists())

    def test_company_registration_success(self):
        """Test successful company registration"""
        response = self.client.post(reverse('company_register'), {
            'username': 'testcompany',
            'email': 'company@test.com',
            'field_of_work': 'Plumbing',
            'password': 'testpass123',
            'password_confirmation': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='testcompany', user_type='company').exists())

    def test_duplicate_email_registration(self):
        """Test registration with duplicate email"""
        User.objects.create_user(
            username='existing',
            email='test@test.com',
            user_type='customer'
        )
        
        response = self.client.post(reverse('customer_register'), {
            'username': 'newuser',
            'email': 'test@test.com',
            'date_of_birth': '1990-01-01',
            'password': 'testpass123',
            'password_confirmation': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)  # Form validation error
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_duplicate_username_registration(self):
        """Test registration with duplicate username"""
        User.objects.create_user(
            username='testuser',
            email='existing@test.com',
            user_type='customer'
        )
        
        response = self.client.post(reverse('customer_register'), {
            'username': 'testuser',
            'email': 'new@test.com',
            'date_of_birth': '1990-01-01',
            'password': 'testpass123',
            'password_confirmation': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)  # Form validation error

    def test_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post(reverse('customer_register'), {
            'username': 'testuser',
            'email': 'test@test.com',
            'date_of_birth': '1990-01-01',
            'password': 'testpass123',
            'password_confirmation': 'differentpass'
        })
        self.assertEqual(response.status_code, 200)  # Form validation error
        self.assertFalse(User.objects.filter(username='testuser').exists())

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer'
        )
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company'
        )

    def test_customer_login_success(self):
        """Test successful customer login"""
        response = self.client.post(reverse('login'), {
            'username': 'customer@test.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_company_login_success(self):
        """Test successful company login"""
        response = self.client.post(reverse('login'), {
            'username': 'company@test.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'customer@test.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout(self):
        """Test user logout"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            date_of_birth='1990-01-01'
        )
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )

    def test_customer_profile_view(self):
        """Test customer profile view"""
        response = self.client.get(reverse('profile', kwargs={'username': 'customer'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'customer@test.com')
        self.assertContains(response, 'January 01, 1990')  # Date is formatted in template

    def test_company_profile_view(self):
        """Test company profile view"""
        response = self.client.get(reverse('profile', kwargs={'username': 'company'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'company@test.com')
        self.assertContains(response, 'Plumbing')

    def test_nonexistent_profile_view(self):
        """Test viewing nonexistent profile"""
        response = self.client.get(reverse('profile', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
