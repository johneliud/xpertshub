from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Service, ServiceRequest, Rating
from users.models import User

class ServiceCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer'
        )
        self.plumber = User.objects.create_user(
            username='plumber',
            email='plumber@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        self.all_in_one = User.objects.create_user(
            username='allinone',
            email='allinone@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='All in One'
        )

    def test_company_can_create_service_in_their_field(self):
        """Test company can create service in their field of work"""
        self.client.login(username='plumber@test.com', password='testpass123')
        response = self.client.post(reverse('create_service'), {
            'name': 'Pipe Repair',
            'description': 'Professional pipe repair service',
            'field': 'Plumbing',
            'price_per_hour': '50.00'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Service.objects.filter(name='Pipe Repair', company=self.plumber).exists())

    def test_all_in_one_company_can_create_any_service(self):
        """Test All in One company can create services in any field"""
        self.client.login(username='allinone@test.com', password='testpass123')
        response = self.client.post(reverse('create_service'), {
            'name': 'Electrical Repair',
            'description': 'Professional electrical service',
            'field': 'Electricity',
            'price_per_hour': '60.00'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Service.objects.filter(name='Electrical Repair', company=self.all_in_one).exists())

    def test_company_cannot_create_service_outside_field(self):
        """Test company cannot create service outside their field"""
        self.client.login(username='plumber@test.com', password='testpass123')
        response = self.client.post(reverse('create_service'), {
            'name': 'Electrical Work',
            'description': 'Electrical service',
            'field': 'Electricity',
            'price_per_hour': '60.00'
        })
        self.assertEqual(response.status_code, 200)  # Form validation error
        self.assertFalse(Service.objects.filter(name='Electrical Work').exists())

    def test_customer_cannot_create_service(self):
        """Test customer cannot access service creation"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('create_service'))
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_anonymous_user_cannot_create_service(self):
        """Test anonymous user cannot create service"""
        response = self.client.get(reverse('create_service'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

class ServiceBrowsingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        self.approved_service = Service.objects.create(
            name='Approved Service',
            description='Test service',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company,
            status='approved'
        )
        self.pending_service = Service.objects.create(
            name='Pending Service',
            description='Test service',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company,
            status='pending'
        )

    def test_home_page_shows_approved_services(self):
        """Test home page displays approved services"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Service')
        self.assertNotContains(response, 'Pending Service')

    def test_all_services_page(self):
        """Test all services page shows only approved services"""
        response = self.client.get(reverse('all_services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Service')
        self.assertNotContains(response, 'Pending Service')

    def test_category_services_page(self):
        """Test category services page"""
        response = self.client.get(reverse('services_by_category', kwargs={'field': 'Plumbing'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Service')
        self.assertNotContains(response, 'Pending Service')

    def test_service_detail_page(self):
        """Test service detail page"""
        response = self.client.get(reverse('service_detail', kwargs={'pk': self.approved_service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Service')
        self.assertContains(response, self.company.username)

    def test_pending_service_detail_not_accessible(self):
        """Test pending service detail is not accessible"""
        response = self.client.get(reverse('service_detail', kwargs={'pk': self.pending_service.pk}))
        self.assertEqual(response.status_code, 404)

class ServiceRequestTests(TestCase):
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

    def test_customer_can_request_service(self):
        """Test customer can request a service"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.post(reverse('request_service', kwargs={'service_id': self.service.pk}), {
            'address': '123 Test Street',
            'service_time_hours': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ServiceRequest.objects.filter(
            service=self.service,
            customer=self.customer,
            address='123 Test Street'
        ).exists())

    def test_company_cannot_request_service(self):
        """Test company cannot request services"""
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('request_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_anonymous_user_cannot_request_service(self):
        """Test anonymous user cannot request service"""
        response = self.client.get(reverse('request_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_service_request_cost_calculation(self):
        """Test service request cost is calculated correctly"""
        self.client.login(username='customer@test.com', password='testpass123')
        self.client.post(reverse('request_service', kwargs={'service_id': self.service.pk}), {
            'address': '123 Test Street',
            'service_time_hours': 3
        })
        
        request = ServiceRequest.objects.get(service=self.service, customer=self.customer)
        expected_cost = self.service.price_per_hour * 3
        self.assertEqual(request.calculated_cost, expected_cost)

    def test_company_can_view_their_service_requests(self):
        """Test company can view requests for their services"""
        ServiceRequest.objects.create(
            service=self.service,
            customer=self.customer,
            address='123 Test Street',
            service_time_hours=2
        )
        
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '123 Test Street')

    def test_customer_cannot_view_service_requests_page(self):
        """Test customer cannot access service requests page"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 302)  # Redirect to home

class ServiceModelTests(TestCase):
    def setUp(self):
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )

    def test_service_string_representation(self):
        """Test service string representation"""
        service = Service.objects.create(
            name='Test Service',
            description='Test description',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company
        )
        self.assertEqual(str(service), 'Test Service - Pending Approval')

    def test_service_default_status(self):
        """Test service default status is pending"""
        service = Service.objects.create(
            name='Test Service',
            description='Test description',
            field='Plumbing',
            price_per_hour=50.00,
            company=self.company
        )
        self.assertEqual(service.status, 'pending')

class ServiceRequestModelTests(TestCase):
    def setUp(self):
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

    def test_service_request_string_representation(self):
        """Test service request string representation"""
        request = ServiceRequest.objects.create(
            service=self.service,
            customer=self.customer,
            address='123 Test Street',
            service_time_hours=2
        )
        expected_str = f"Request for {self.service.name} by {self.customer.username}"
        self.assertEqual(str(request), expected_str)

    def test_calculated_cost_property(self):
        """Test calculated cost property"""
        request = ServiceRequest.objects.create(
            service=self.service,
            customer=self.customer,
            address='123 Test Street',
            service_time_hours=3
        )
        expected_cost = self.service.price_per_hour * 3
        self.assertEqual(request.calculated_cost, expected_cost)

class RatingSystemTests(TestCase):
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

    def test_customer_can_rate_service(self):
        """Test customer can rate a service"""
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.post(reverse('rate_service', kwargs={'service_id': self.service.pk}), {
            'rating': 5,
            'review': 'Excellent service!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Rating.objects.filter(
            service=self.service,
            customer=self.customer,
            rating=5
        ).exists())

    def test_customer_cannot_rate_same_service_twice(self):
        """Test customer cannot rate the same service twice"""
        Rating.objects.create(
            service=self.service,
            customer=self.customer,
            rating=4,
            review='Good service'
        )
        
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('rate_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected away

    def test_company_cannot_rate_service(self):
        """Test company cannot rate services"""
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('rate_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected away

    def test_anonymous_user_cannot_rate_service(self):
        """Test anonymous user cannot rate service"""
        response = self.client.get(reverse('rate_service', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected to login

    def test_service_average_rating_calculation(self):
        """Test service average rating is calculated correctly"""
        Rating.objects.create(service=self.service, customer=self.customer, rating=5)
        
        customer2 = User.objects.create_user(
            username='customer2',
            email='customer2@test.com',
            password='testpass123',
            user_type='customer'
        )
        Rating.objects.create(service=self.service, customer=customer2, rating=3)
        
        self.assertEqual(self.service.average_rating, 4.0)  # (5+3)/2 = 4.0
        self.assertEqual(self.service.rating_count, 2)

    def test_service_detail_shows_ratings(self):
        """Test service detail page shows ratings"""
        Rating.objects.create(
            service=self.service,
            customer=self.customer,
            rating=5,
            review='Great service!'
        )
        
        response = self.client.get(reverse('service_detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great service!')
        self.assertContains(response, 'customer')  # Customer username

    def test_rating_model_string_representation(self):
        """Test rating model string representation"""
        rating = Rating.objects.create(
            service=self.service,
            customer=self.customer,
            rating=4,
            review='Good service'
        )
        expected_str = f"{self.customer.username} rated {self.service.name}: 4/5"
        self.assertEqual(str(rating), expected_str)

class PaginationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = User.objects.create_user(
            username='company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        
        # Create 10 services to test pagination (paginate_by = 6)
        self.services = []
        for i in range(10):
            service = Service.objects.create(
                name=f'Test Service {i+1}',
                description=f'Test service {i+1}',
                field='Plumbing',
                price_per_hour=50.00 + i,
                company=self.company,
                status='approved'
            )
            self.services.append(service)

    def test_all_services_pagination(self):
        """Test pagination on all services page"""
        response = self.client.get(reverse('all_services'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['services']), 6)  # First page should have 6 services
        
        # Test second page
        response = self.client.get(reverse('all_services') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 4)  # Second page should have 4 services

    def test_category_services_pagination(self):
        """Test pagination on category services page"""
        response = self.client.get(reverse('services_by_category', kwargs={'field': 'Plumbing'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['services']), 6)  # First page should have 6 services

    def test_pagination_invalid_page(self):
        """Test pagination with invalid page number"""
        response = self.client.get(reverse('all_services') + '?page=999')
        self.assertEqual(response.status_code, 404)  # Should return 404 for invalid page

    def test_pagination_page_one_redirect(self):
        """Test pagination page 1 behavior"""
        response = self.client.get(reverse('all_services') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 1)
