from django.shortcuts import get_object_or_404
from products.models import Product


def bag_content(request):
    bag = request.session.get('bag', {})
    bag_items = []

    total_price = 0

    for product_id, quantity in bag.items():
        product = get_object_or_404(Product, id=product_id)
        bag_items.append({
            'product': product,
            'quantity': quantity,
            'bag_total': product.price * quantity
        })

        total_price += product.price * quantity

    context = {
        'total_price': total_price,
        'bag_items': bag_items,
    }

    return context
