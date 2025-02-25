from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import Food

class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model = OrderItem
        fields = ['food', 'food_name', 'quantity', 'rating']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'status', 'order_time', 'items']

class OrderItemRequestSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderRequestSerializer(serializers.Serializer):
    food_items = serializers.ListField(
        child=OrderItemRequestSerializer(), 
        allow_empty=False
    )