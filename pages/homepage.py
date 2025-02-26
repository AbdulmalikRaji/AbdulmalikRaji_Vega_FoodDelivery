from django.shortcuts import render
from restaurants.models import Food
import random

def homepage(request):
    # Retrieve all food items
    all_foods = list(Food.objects.all())

    # Select 4 random food items or fewer
    featured_foods = Food.objects.order_by('?')[:4]

    context = {
        'featured_foods': featured_foods
    }

    return render(request, 'homepage.html', context)
