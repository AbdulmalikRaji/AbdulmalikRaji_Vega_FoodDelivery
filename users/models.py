from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    DELIVERY_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    delivery_location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    role = models.CharField(max_length=5, choices=DELIVERY_ROLES, default='user')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
