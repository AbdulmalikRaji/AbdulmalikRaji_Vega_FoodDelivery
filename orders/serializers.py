from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import Food

class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model = OrderItem
        fields = ['food', 'food_name', 'quantity', 'rating', 'comment']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant = serializers.ReadOnlyField(source='restaurant.name')

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

class RatingSerializer(serializers.Serializer):
    id = serializers.IntegerField() 
    order_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True, max_length=200)
    
    def validate(self, data):
        order_id = data.get('order_id')
        order_item_id = data.get('id')

        # Check if the order is delivered
        try:
            order = Order.objects.get(id=order_id, status='delivered')
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order is not delivered or does not exist.")

        # Check if the user owns this order
        if self.context['request'].user != order.user:
            raise serializers.ValidationError("You do not have permission to rate this order.")
        
        # Check if this order item has been rated before
        from orders.models import OrderItem  # Import here to avoid circular import
        try:
            order_item = OrderItem.objects.get(id=order_item_id, order=order)
            if order_item.rating is not None:  # Check if a rating already exists
                raise serializers.ValidationError("This item has already been rated.")
        except OrderItem.DoesNotExist:
            raise serializers.ValidationError("Order item does not exist.")
        
        return data