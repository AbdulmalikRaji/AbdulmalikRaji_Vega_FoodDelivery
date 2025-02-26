from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=25, choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available')

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image_url = models.URLField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return self.name
