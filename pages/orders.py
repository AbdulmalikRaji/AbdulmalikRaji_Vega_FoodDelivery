from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import timedelta
from django.utils.timezone import localtime
from orders.models import Order, OrderItem

@login_required
def orders_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_time')

    order_data = []
    for order in orders:
        delivery_time = order.order_time + timedelta(minutes=15)  
        order_items = []

        for item in order.items.all():
            order_items.append({
                'id': item.id,
                'food_name': item.food.name,
                'quantity': item.quantity,
                'rating': item.rating,
                'comment': item.comment,
            })

        order_data.append({
            'id': order.id,
            'restaurant': order.restaurant.name,
            'restaurant_address': order.restaurant.location,
            'status': order.status.capitalize(),
            'order_time': localtime(order.order_time).strftime("%Y-%m-%d %H:%M"),
            'delivery_time': localtime(delivery_time).strftime("%Y-%m-%d %H:%M"),
            'items': order_items,
        })

    return render(request, 'orders.html', {'orders': order_data})
