from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    DELIVERY_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    delivery_location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    role = models.CharField(max_length=5, choices=DELIVERY_ROLES, default='user')

    def __str__(self):
        return self.username
