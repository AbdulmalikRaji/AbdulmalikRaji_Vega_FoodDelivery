from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from restaurants.models import Food, Restaurant
from orders.models import Order, OrderItem
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class OrderTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="TestPass123", is_verified=True)
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", status="available", latitude=0, longitude=0)
        self.food = Food.objects.create(name="Burger", price=10, rating=4.5)
        self.order = Order.objects.create(user=self.user, restaurant=self.restaurant, status="delivered")
        self.order_item = OrderItem.objects.create(order=self.order, food=self.food, quantity=2)

        # Authenticate user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

    def test_create_order(self):
        """Test creating an order"""
        url = reverse('order-create')
        data = {"food_items": [{"food_id": self.food.id, "quantity": 1}]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orders(self):
        """Test retrieving orders"""
        url = reverse('my-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_submit_rating(self):
        """Test submitting a rating"""
        url = reverse('rate-order')
        data = {"id": self.order_item.id, "order_id": self.order.id, "rating": 5, "comment": "Great food!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
