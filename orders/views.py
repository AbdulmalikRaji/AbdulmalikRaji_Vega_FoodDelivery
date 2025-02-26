from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderRequestSerializer, RatingSerializer
from restaurants.models import Food, Restaurant
from users.models import CustomUser
from django.utils import timezone
from datetime import timedelta
import threading
from django.db.models import F, Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    
class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order_item_id = serializer.validated_data['id']
            rating = serializer.validated_data['rating']
            comment = serializer.validated_data.get('comment', '')

            # Get the order and item
            ordered_food = OrderItem.objects.get(id=order_item_id)
            

            # Update each item with the rating and comment
            ordered_food.rating = rating
            if ordered_food.comment:
                ordered_food.comment = comment

            ordered_food.save()

            # Calculate the new average rating for the food
            food_id = ordered_food.food_id
            food = Food.objects.get(id=food_id)
            avg_rating = OrderItem.objects.filter(food=food).aggregate(Avg('rating'))['rating__avg']
            food.rating = round(avg_rating, 2)  # Round to 2 decimal places
            food.save()

            return Response({"message": "Rating submitted successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)