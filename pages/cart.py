from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from restaurants.models import Food
import json
from django.http import JsonResponse
import requests
from rest_framework.authtoken.models import Token


def add_to_cart(request, id):
    food = get_object_or_404(Food, id=id)
    cart = request.session.get('cart', {})

    # Increment if already in cart, otherwise set to 1
    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    messages.success(request, f"{food.name} added to cart!")
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('menu-page')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []

    # Get food items and their quantities
    for food_id, quantity in cart.items():
        food = get_object_or_404(Food, id=food_id)
        cart_items.append({
            'food': food,
            'quantity': quantity,
            'total_price': food.price * quantity
        })

    total_amount = sum(item['total_price'] for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount
    }
    return render(request, 'cart.html', context)

def update_cart(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        cart = request.session.get('cart', {})

        if action == 'increase':
            cart[str(id)] = cart.get(str(id), 0) + 1
        elif action == 'decrease':
            if str(id) in cart:
                cart[str(id)] -= 1
                if cart[str(id)] <= 0:
                    del cart[str(id)]
        elif action == 'delete':
            if str(id) in cart:
                del cart[str(id)]

        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def checkout_order(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to checkout.')
        return JsonResponse({'error': 'You must be logged in to checkout.'}, status=401)

    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'error': 'Cart is empty.'}, status=400)

    food_items = [{'food_id': int(food_id), 'quantity': quantity} for food_id, quantity in cart.items()]

    api_url = request.build_absolute_uri('/api/orders/order/')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {request.session["access_token"]}'  # Get token from session
    }
    payload = {
        'food_items': food_items
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        # Clear the cart after successful order
        request.session['cart'] = {}
        return JsonResponse({'message': 'Order placed successfully!'})
    else:
        # Return the exact error from the API
        try:
            error_message = response.json().get('error', 'Failed to place order.')
        except ValueError:
            error_message = 'Failed to place order.'
        return JsonResponse({'error': error_message}, status=response.status_code)


