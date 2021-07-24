from shop.models import Cart

def add_variable_to_context(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total = 0
        for cart in carts:
            total = total + cart.product.price * cart.quantity
        return {
            'carts': carts,
            'total': total,
            'count': carts.count(),
        }
    else:
        return {
            'carts': 'cart',
            'total': 'total'
        }