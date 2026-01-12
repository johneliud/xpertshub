from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('company', 'Company'),
    )
    FIELD_OF_WORK_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('All in One', 'All in One'),
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

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    date_of_birth = models.DateField(null=True, blank=True)
    field_of_work = models.CharField(max_length=50, choices=FIELD_OF_WORK_CHOICES, null=True, blank=True)
