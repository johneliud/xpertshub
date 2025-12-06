from django.db import models
from django.conf import settings

class Service(models.Model):
    FIELD_OF_WORK_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('Housekeeping', 'Housekeeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    field = models.CharField(max_length=50, choices=FIELD_OF_WORK_CHOICES)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services_provided',
        limit_choices_to={'user_type': 'company'}
    )

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests',
        limit_choices_to={'user_type': 'customer'}
    )
    address = models.TextField()
    service_time_hours = models.DecimalField(max_digits=5, decimal_places=2)
    date_requested = models.DateTimeField(auto_now_add=True)

    @property
    def calculated_cost(self):
        return self.service.price_per_hour * self.service_time_hours

    def __str__(self):
        return f"Request for {self.service.name} by {self.customer.username}"
