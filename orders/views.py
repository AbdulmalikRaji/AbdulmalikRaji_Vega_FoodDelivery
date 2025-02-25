from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderRequestSerializer
from restaurants.models import Food, Restaurant
from users.models import CustomUser
from django.utils import timezone
from datetime import timedelta
import threading
from django.db.models import F
from rest_framework.permissions import IsAuthenticated

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        # Validate the request data
        serializer = OrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        food_items = serializer.validated_data['food_items']

        # Get nearest restaurant with available courier
        nearest_restaurant = Restaurant.objects.filter(status='available').order_by(
            ((F('latitude') - user.latitude) ** 2 + (F('longitude') - user.longitude) ** 2)
        ).first()

        if not nearest_restaurant:
            return Response({"error": "No available restaurant nearby."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=user, restaurant=nearest_restaurant, status='processing')

        # Add food items to the order
        for item in food_items:
            food_id = item['food_id']
            quantity = item['quantity']
            food_item = Food.objects.get(id=food_id)
            OrderItem.objects.create(order=order, food=food_item, quantity=quantity)

        # Engage restaurant
        nearest_restaurant.status = 'unavailable'
        nearest_restaurant.save()

        # Release restaurant after 15 minutes
        release_restaurant_after_timeout(nearest_restaurant.id)

        return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)

def release_restaurant_after_timeout(restaurant_id, timeout=900):
    def release():
        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.status = 'available'
        restaurant.save()
    timer = threading.Timer(timeout, release)
    timer.start()

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        # Get the current authenticated user
        user = self.request.user
        # Return only the orders made by this user
        return Order.objects.filter(user=user)