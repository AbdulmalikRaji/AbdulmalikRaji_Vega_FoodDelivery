from celery import shared_task
from orders.models import Order
from restaurants.models import Restaurant

@shared_task
def release_restaurant(restaurant_id, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = "delivered"
        order.save()

        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.status = "available"
        restaurant.save()
        return f"Restaurant {restaurant.name} is now available."
    except Restaurant.DoesNotExist:
        return f"Restaurant with ID:{restaurant_id} not found."
