from celery import shared_task
from restaurants.models import Restaurant

@shared_task
def release_restaurant(restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.status = "available"
        restaurant.save()
        return f"Restaurant {restaurant_id} is now available."
    except Restaurant.DoesNotExist:
        return f"Restaurant {restaurant_id} not found."
