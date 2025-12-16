from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from services.models import Service

class NavigationTests(TestCase):
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
            user_type='company',
            field_of_work='Plumbing'
        )

    def test_home_page_accessible(self):
        """Test home page is accessible"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_accessible(self):
        """Test about page is accessible"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_navigation_links_for_anonymous_user(self):
        """Test navigation shows correct links for anonymous users"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Should contain login/register links
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Customer')  # Registration button text
        self.assertContains(response, 'Provider')  # Registration button text

    def test_navigation_links_for_authenticated_customer(self):
        """Test navigation shows correct links for authenticated customers"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Should contain profile and logout links
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Logout')

    def test_navigation_links_for_authenticated_company(self):
        """Test navigation shows correct links for authenticated companies"""
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Should contain profile, logout, and create service links
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Create Service')

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        # Create some approved services
        self.service1 = Service.objects.create(
            name='Popular Service',
            description='Most requested service',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company,
            status='approved'
        )
        self.service2 = Service.objects.create(
            name='Another Service',
            description='Another service',
            field='Plumbing',
            price_per_hour=60.00,
            company=self.company,
            status='approved'
        )

    def test_home_page_displays_featured_services(self):
        """Test home page displays featured services"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Popular Service')
        self.assertContains(response, 'Another Service')

    def test_home_page_service_links(self):
        """Test home page contains links to service details"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        service_url = reverse('service_detail', kwargs={'pk': self.service1.pk})
        self.assertContains(response, service_url)

class ErrorPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_404_page(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_service_returns_404(self):
        """Test accessing nonexistent service returns 404"""
        response = self.client.get(reverse('service_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_profile_returns_404(self):
        """Test accessing nonexistent profile returns 404"""
        response = self.client.get(reverse('profile', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)

class URLRoutingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_routing_home(self):
        """Test home URL routing"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_routing_about(self):
        """Test about URL routing"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_url_routing_auth_pages(self):
        """Test authentication URL routing"""
        # Login page
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        
        # Customer register page
        response = self.client.get('/auth/register/customer/')
        self.assertEqual(response.status_code, 200)
        
        # Company register page
        response = self.client.get('/auth/register/company/')
        self.assertEqual(response.status_code, 200)

    def test_url_routing_services_pages(self):
        """Test services URL routing"""
        # All services page
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        
        # Category services page
        response = self.client.get('/services/category/Plumbing/')
        self.assertEqual(response.status_code, 200)

class SecurityTests(TestCase):
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
            user_type='company',
            field_of_work='Plumbing'
        )
        self.service = Service.objects.create(
            name='Test Service',
            description='Test service',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company,
            status='approved'
        )

    def test_unauthorized_access_to_create_service(self):
        """Test unauthorized access to create service is blocked"""
        # Anonymous user
        response = self.client.get(reverse('create_service'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Customer user
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('create_service'))
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_unauthorized_access_to_service_requests(self):
        """Test unauthorized access to service requests is blocked"""
        # Anonymous user
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Customer user
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_unauthorized_access_to_request_service(self):
        """Test unauthorized access to request service is blocked"""
        # Anonymous user
        response = self.client.get(reverse('request_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Company user
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('request_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to home
