from django.shortcuts import render
from rest_framework import generics
from .models import Food
from .serializers import FoodSerializer

class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class FoodDetailView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'id'
