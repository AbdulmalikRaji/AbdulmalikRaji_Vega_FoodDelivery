from django.shortcuts import render
from restaurants.models import Food
import random

def homepage(request):
    # Select 4 random food items or fewer
    featured_foods = Food.objects.order_by('?')[:4]

    context = {
        'featured_foods': featured_foods
    }

    return render(request, 'homepage.html', context)
