from django.urls import path
from .views import FoodListView, FoodDetailView

urlpatterns = [
    path('food/', FoodListView.as_view(), name='food-list'),
    path('food/<int:id>/', FoodDetailView.as_view(), name='food-item'),
]
