from django.utils import timezone
from orders.models import Order
from datetime import timedelta

def check_expired_orders():
    # After 15 minutes
    expiration_time = timezone.now() - timedelta(minutes=15)
    
    # Get all processing orders older than 15 minutes
    expired_orders = Order.objects.filter(status='processing', order_time__lte=expiration_time)
    
    for order in expired_orders:
        order.status = 'delivered'
        order.save()
        
        restaurant = order.restaurant
        restaurant.status = 'available'
        restaurant.save()

    print(f"{expired_orders.count()} orders marked as delivered.")
