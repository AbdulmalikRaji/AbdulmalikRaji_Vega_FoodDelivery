from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from restaurants.models import Food, Restaurant

class FoodTests(APITestCase):

    def setUp(self):
        """Set up test food items"""
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", status="available", latitude=0, longitude=0)
        self.food1 = Food.objects.create(name="Burger", price=10, rating=4.5)
        self.food2 = Food.objects.create(name="Pizza", price=15, rating=3.5)

    def test_list_food_items(self):
        """Test retrieving food items"""
        url = reverse('food-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_filter_food_by_name(self):
        """Test filtering food by name"""
        url = reverse('food-list') + "?name=burger"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_filter_food_by_price(self):
        """Test filtering food by price"""
        url = reverse('food-list') + "?min_price=5&max_price=12"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_filter_food_by_rating(self):
        """Test filtering food by minimum rating"""
        url = reverse('food-list') + "?min_rating=4"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_food_detail(self):
        """Test retrieving a specific food item"""
        url = reverse('food-item', kwargs={'id': self.food1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Burger")

