from django.shortcuts import render, get_object_or_404
from restaurants.models import Food
from orders.models import OrderItem 
from django.views import View

class MenuItemView(View):
    def get(self, request, id, *args, **kwargs):
        food = get_object_or_404(Food, id=id)
        comments = (
            OrderItem.objects.filter(food=food, rating__isnull=False)
            .select_related('order__user')
            .order_by('-order__order_time')[:10]
        )
        context = {
            'food': food,
            'comments': comments,
        }
        return render(request, 'menu_item.html', context)
