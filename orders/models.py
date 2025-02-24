from django.db import models
from users.models import CustomUser
from restaurants.models import Food, Restaurant
from django.utils import timezone
from django.db.models import Avg

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(Food, through='OrderItem')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.food.name} (x{self.quantity})"



# def update_food_rating(food):
#     average_rating = OrderItem.objects.filter(food=food, rating__isnull=False).aggregate(Avg('rating'))['rating__avg']
#     food.rating = round(average_rating, 2) if average_rating else 0.00
#     food.save()
