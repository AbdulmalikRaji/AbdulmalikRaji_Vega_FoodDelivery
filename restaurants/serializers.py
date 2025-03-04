from rest_framework import serializers
from .models import Food
from orders.models import OrderItem
from users.models import CustomUser

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='order.user.username', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['username', 'rating', 'comment']

class FoodSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'description', 'price', 'rating', 'image_url', 'comments']

    def get_comments(self, obj):
        # Get the number of comments to show, default to 1
        request = self.context.get('request')
        num_comments = int(request.query_params.get('num_comments', 1))
        num_comments = min(max(num_comments, 1), 5)

        # Fetch comments for this food item along with user who commented
        comments = (
            OrderItem.objects
            .filter(food=obj, comment__isnull=False)
            .select_related('order__user')  # join with user
            .order_by('-id')[:num_comments]
        )
        return CommentSerializer(comments, many=True).data
