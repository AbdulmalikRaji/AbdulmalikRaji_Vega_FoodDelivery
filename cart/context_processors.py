def cart_count(request):
    cart = request.session.get('cart', {})
    count = len(cart)  # number of items
    return {'cart_count': count}
