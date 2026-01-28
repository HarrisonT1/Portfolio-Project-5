from django.shortcuts import get_object_or_404
from products.models import Product


def bag_content(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total_bag_items = 0

    total_price = 0

    for product_slug, quantity in list(bag.items()):
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            bag.pop(product_slug)
            continue

        bag_items.append({
            'product': product,
            'quantity': quantity,
            'bag_total': product.price * quantity
        })

        total_price += product.price * quantity
        total_bag_items += quantity

    context = {
        'total_price': total_price,
        'bag_items': bag_items,
        'total_bag_items': total_bag_items,
    }

    return context
