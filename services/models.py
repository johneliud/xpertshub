from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

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

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    field = models.CharField(max_length=50, choices=FIELD_OF_WORK_CHOICES)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_services'
    )
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services_provided',
        limit_choices_to={'user_type': 'company'}
    )

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0

    @property
    def rating_count(self):
        return self.ratings.count()

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

class Rating(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings_given',
        limit_choices_to={'user_type': 'customer'}
    )
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'customer')

    def __str__(self):
        return f"{self.customer.username} rated {self.service.name}: {self.rating}/5"
