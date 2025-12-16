"""
Integration tests for complete user workflows in XpertsHub
"""
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from services.models import Service, ServiceRequest

class CompleteWorkflowIntegrationTest(TestCase):
    """Test complete user workflows from registration to service completion"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_customer_workflow(self):
        """Test complete customer workflow: register -> login -> browse -> request service"""
        
        # 1. Customer Registration
        response = self.client.post(reverse('customer_register'), {
            'username': 'john_customer',
            'email': 'john@customer.com',
            'date_of_birth': '1990-05-15',
            'password': 'securepass123',
            'password_confirmation': 'securepass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Verify customer was created
        customer = User.objects.get(username='john_customer')
        self.assertEqual(customer.user_type, 'customer')
        self.assertEqual(customer.email, 'john@customer.com')
        
        # 2. Customer Login
        response = self.client.post(reverse('login'), {
            'username': 'john@customer.com',
            'password': 'securepass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # 3. Browse Services (need to create a service first)
        # Create a company and service for testing
        company = User.objects.create_user(
            username='plumber_co',
            email='plumber@company.com',
            password='companypass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        
        service = Service.objects.create(
            name='Emergency Plumbing',
            description='24/7 emergency plumbing service',
            field='Plumbing',
            price_per_hour=75.00,
            company=company,
            status='approved'
        )
        
        # Browse all services
        response = self.client.get(reverse('all_services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Emergency Plumbing')
        
        # View service detail
        response = self.client.get(reverse('service_detail', kwargs={'pk': service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Emergency Plumbing')
        self.assertContains(response, 'KES 75.00')  # Price format in template
        
        # 4. Request Service
        response = self.client.post(reverse('request_service', kwargs={'service_id': service.pk}), {
            'address': '123 Main Street, Anytown, USA',
            'service_time_hours': 2.5
        })
        self.assertEqual(response.status_code, 302)  # Redirect after request
        
        # Verify service request was created
        service_request = ServiceRequest.objects.get(customer=customer, service=service)
        self.assertEqual(service_request.address, '123 Main Street, Anytown, USA')
        self.assertEqual(service_request.service_time_hours, 2.5)
        self.assertEqual(service_request.calculated_cost, 187.50)  # 75 * 2.5
        
        # 5. View Profile with Service Request
        response = self.client.get(reverse('profile', kwargs={'username': 'john_customer'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'john@customer.com')
        self.assertContains(response, 'Emergency Plumbing')
    
    def test_complete_company_workflow(self):
        """Test complete company workflow: register -> login -> create service -> view requests"""
        
        # 1. Company Registration
        response = self.client.post(reverse('company_register'), {
            'username': 'elite_painters',
            'email': 'contact@elitepainters.com',
            'field_of_work': 'Painting',
            'password': 'painterpro123',
            'password_confirmation': 'painterpro123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Verify company was created
        company = User.objects.get(username='elite_painters')
        self.assertEqual(company.user_type, 'company')
        self.assertEqual(company.field_of_work, 'Painting')
        
        # 2. Company Login
        response = self.client.post(reverse('login'), {
            'username': 'contact@elitepainters.com',
            'password': 'painterpro123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # 3. Create Service
        response = self.client.post(reverse('create_service'), {
            'name': 'Interior House Painting',
            'description': 'Professional interior painting with premium materials',
            'field': 'Painting',
            'price_per_hour': 45.00
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify service was created
        service = Service.objects.get(company=company)
        self.assertEqual(service.name, 'Interior House Painting')
        self.assertEqual(service.status, 'pending')  # Default status
        
        # 4. Approve service (simulate admin approval)
        service.status = 'approved'
        service.save()
        
        # 5. Create a customer and service request for testing
        customer = User.objects.create_user(
            username='homeowner',
            email='homeowner@email.com',
            password='homepass123',
            user_type='customer'
        )
        
        ServiceRequest.objects.create(
            service=service,
            customer=customer,
            address='456 Oak Avenue, Hometown, USA',
            service_time_hours=8.0
        )
        
        # 6. View Service Requests
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '456 Oak Avenue')
        self.assertContains(response, 'homeowner')
        
        # 7. View Company Profile
        response = self.client.get(reverse('profile', kwargs={'username': 'elite_painters'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'contact@elitepainters.com')
        self.assertContains(response, 'Interior House Painting')
    
    def test_all_in_one_company_workflow(self):
        """Test All in One company can create services in any field"""
        
        # 1. Register All in One Company
        response = self.client.post(reverse('company_register'), {
            'username': 'total_solutions',
            'email': 'info@totalsolutions.com',
            'field_of_work': 'All in One',
            'password': 'allservices123',
            'password_confirmation': 'allservices123'
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Login
        self.client.login(username='info@totalsolutions.com', password='allservices123')
        
        # 3. Create services in different fields
        fields_to_test = ['Plumbing', 'Electricity', 'Painting', 'Housekeeping']
        
        for field in fields_to_test:
            response = self.client.post(reverse('create_service'), {
                'name': f'Professional {field} Service',
                'description': f'Expert {field.lower()} solutions',
                'field': field,
                'price_per_hour': 50.00
            })
            self.assertEqual(response.status_code, 302)  # Should succeed
        
        # Verify all services were created
        company = User.objects.get(username='total_solutions')
        services = Service.objects.filter(company=company)
        self.assertEqual(services.count(), 4)
        
        # Verify services in different fields
        service_fields = list(services.values_list('field', flat=True))
        for field in fields_to_test:
            self.assertIn(field, service_fields)
    
    def test_security_workflow(self):
        """Test security restrictions are properly enforced"""
        
        # Create test users
        customer = User.objects.create_user(
            username='test_customer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer'
        )
        
        company = User.objects.create_user(
            username='test_company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        
        service = Service.objects.create(
            name='Test Service',
            description='Test service',
            field='Plumbing',
            price_per_hour=50.00,
            company=company,
            status='approved'
        )
        
        # Test 1: Customer cannot create services
        self.client.login(username='customer@test.com', password='testpass123')
        response = self.client.get(reverse('create_service'))
        self.assertEqual(response.status_code, 302)  # Redirected away
        
        # Test 2: Customer cannot view service requests
        response = self.client.get(reverse('service_requests'))
        self.assertEqual(response.status_code, 302)  # Redirected away
        
        # Test 3: Company cannot request services
        self.client.login(username='company@test.com', password='testpass123')
        response = self.client.get(reverse('request_service', kwargs={'service_id': service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected away
        
        # Test 4: Anonymous users cannot access restricted pages
        self.client.logout()
        
        restricted_urls = [
            reverse('create_service'),
            reverse('service_requests'),
            reverse('request_service', kwargs={'service_id': service.pk})
        ]
        
        for url in restricted_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirected to login
    
    def test_error_handling_workflow(self):
        """Test proper error handling for various scenarios"""
        
        # Test 1: Accessing non-existent service
        response = self.client.get(reverse('service_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
        
        # Test 2: Accessing non-existent profile
        response = self.client.get(reverse('profile', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
        
        # Test 3: Accessing pending service detail
        company = User.objects.create_user(
            username='test_company',
            email='company@test.com',
            password='testpass123',
            user_type='company',
            field_of_work='Plumbing'
        )
        
        pending_service = Service.objects.create(
            name='Pending Service',
            description='This service is pending approval',
            field='Plumbing',
            price_per_hour=50.00,
            company=company,
            status='pending'  # Not approved
        )
        
        response = self.client.get(reverse('service_detail', kwargs={'pk': pending_service.pk}))
        self.assertEqual(response.status_code, 404)  # Should not be accessible
