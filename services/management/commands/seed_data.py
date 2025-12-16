from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from services.models import Service, ServiceRequest, Rating
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed database with sample users and services'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create 20 customers
        customers = []
        customer_names = [
            'john_doe', 'jane_smith', 'mike_johnson', 'sarah_wilson', 'david_brown',
            'lisa_davis', 'chris_miller', 'amanda_garcia', 'kevin_martinez', 'nicole_anderson',
            'ryan_taylor', 'jessica_thomas', 'brandon_jackson', 'ashley_white', 'justin_harris',
            'stephanie_martin', 'tyler_thompson', 'rachel_clark', 'jordan_lewis', 'michelle_walker'
        ]

        for i, name in enumerate(customer_names):
            customer = User.objects.create_user(
                username=name,
                email=f'{name}@customer.com',
                password='password123',
                user_type='customer',
                date_of_birth=datetime(1980 + i, (i % 12) + 1, (i % 28) + 1).date()
            )
            customers.append(customer)

        # Create 20 companies
        companies = []
        company_data = [
            ('elite_plumbers', 'Plumbing'), ('ace_electricians', 'Electricity'), ('pro_painters', 'Painting'),
            ('clean_masters', 'Housekeeping'), ('garden_experts', 'Gardening'), ('wood_crafters', 'Carpentry'),
            ('cool_air_tech', 'Air Conditioner'), ('lock_specialists', 'Locks'), ('design_pros', 'Interior Design'),
            ('home_fixers', 'Home Machines'), ('water_heater_pros', 'Water Heaters'), ('total_solutions', 'All in One'),
            ('quick_plumbers', 'Plumbing'), ('spark_electric', 'Electricity'), ('color_masters', 'Painting'),
            ('tidy_homes', 'Housekeeping'), ('green_thumbs', 'Gardening'), ('custom_wood', 'Carpentry'),
            ('arctic_cooling', 'Air Conditioner'), ('secure_locks', 'Locks')
        ]

        for i, (name, field) in enumerate(company_data):
            company = User.objects.create_user(
                username=name,
                email=f'{name}@company.com',
                password='password123',
                user_type='company',
                field_of_work=field
            )
            companies.append(company)

        # Create services for each company
        service_templates = {
            'Plumbing': ['Emergency Plumbing', 'Pipe Installation', 'Drain Cleaning', 'Leak Repair'],
            'Electricity': ['Wiring Installation', 'Electrical Repair', 'Panel Upgrade', 'Outlet Installation'],
            'Painting': ['Interior Painting', 'Exterior Painting', 'Wall Preparation', 'Color Consultation'],
            'Housekeeping': ['Deep Cleaning', 'Regular Cleaning', 'Move-in Cleaning', 'Office Cleaning'],
            'Gardening': ['Lawn Maintenance', 'Garden Design', 'Tree Pruning', 'Landscaping'],
            'Carpentry': ['Custom Furniture', 'Cabinet Installation', 'Deck Building', 'Door Installation'],
            'Air Conditioner': ['AC Installation', 'AC Repair', 'AC Maintenance', 'Duct Cleaning'],
            'Locks': ['Lock Installation', 'Lock Repair', 'Key Duplication', 'Security Upgrade'],
            'Interior Design': ['Room Design', 'Space Planning', 'Furniture Selection', 'Color Schemes'],
            'Home Machines': ['Appliance Repair', 'Installation Service', 'Maintenance Check', 'Troubleshooting'],
            'Water Heaters': ['Heater Installation', 'Heater Repair', 'Maintenance Service', 'Replacement'],
            'All in One': ['Complete Home Service', 'Multi-Service Package', 'Home Renovation', 'Maintenance Bundle']
        }

        services = []
        for company in companies:
            field = company.field_of_work
            if field == 'All in One':
                # All in One companies can offer services from any field
                all_services = []
                for field_services in service_templates.values():
                    all_services.extend(field_services)
                available_services = random.sample(all_services, 3)
                service_fields = ['Plumbing', 'Electricity', 'Painting', 'Housekeeping']
            else:
                available_services = service_templates.get(field, ['General Service'])
                service_fields = [field]

            for i, service_name in enumerate(available_services[:3]):  # Max 3 services per company
                service_field = random.choice(service_fields) if field == 'All in One' else field
                service = Service.objects.create(
                    name=f'{service_name} by {company.username}',
                    description=f'Professional {service_name.lower()} service provided by experienced technicians.',
                    field=service_field,
                    price_per_hour=random.uniform(25.0, 100.0),
                    company=company,
                    status='approved',
                    date_created=timezone.now() - timedelta(days=random.randint(1, 90))
                )
                services.append(service)

        # Create service requests
        for _ in range(30):
            customer = random.choice(customers)
            service = random.choice(services)
            ServiceRequest.objects.create(
                service=service,
                customer=customer,
                address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm Dr", "Maple Ln"])}',
                service_time_hours=random.uniform(1.0, 8.0),
                date_requested=timezone.now() - timedelta(days=random.randint(1, 30))
            )

        # Create ratings
        for _ in range(40):
            customer = random.choice(customers)
            service = random.choice(services)
            
            # Check if this customer has already rated this service
            if not Rating.objects.filter(service=service, customer=customer).exists():
                Rating.objects.create(
                    service=service,
                    customer=customer,
                    rating=random.randint(3, 5),  # Mostly positive ratings
                    review=random.choice([
                        'Excellent service! Highly recommended.',
                        'Great work, very professional.',
                        'Good quality service, will use again.',
                        'Satisfied with the work done.',
                        'Professional and timely service.',
                        '',  # Some ratings without reviews
                        'Outstanding work quality.',
                        'Very pleased with the results.'
                    ]),
                    date_created=timezone.now() - timedelta(days=random.randint(1, 60))
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(customers)} customers\n'
                f'- {len(companies)} companies\n'
                f'- {len(services)} services\n'
                f'- 30 service requests\n'
                f'- 40 ratings'
            )
        )
