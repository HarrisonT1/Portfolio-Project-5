from django.shortcuts import get_object_or_404
from decimal import Decimal
from products.models import Product
from pick_and_mix.models import PickAndMixBag


def bag_content(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total_bag_items = 0

    total_price = Decimal('0.00')

    for item_id, item in bag.items():
        if isinstance(item, dict) and 'pick_and_mix' in item:
            pnm = item['pick_and_mix']
            friendly_display = []

            for slug, data in pnm.get('items', {}).items():
                try:
                    product = Product.objects.get(slug=slug)
                except Product.DoesNotExist:
                    continue

                friendly_display.append({
                    'name': product.name,
                    'quantity': data['quantity'],
                    'total_weight': data['total_weight'],
                })

            bag_object = PickAndMixBag.objects.get(id=pnm.get('bag_id'))

            bag_items.append({
                'type': 'pick_and_mix',
                'item_id': item_id,
                'quantity': item.get('quantity', 1),
                'price': Decimal(item.get('price', 0)),
                'bag_id': pnm.get('bag_id'),
                'bag_name': bag_object.name,
                'max_weight': bag_object.max_weight_in_grams,
                'items': friendly_display,
            })
            total_price += Decimal(item.get('price', 0)) * item.get('quantity', 1)
            total_bag_items += item.get('quantity', 1)
        else:
            try:
                product = Product.objects.get(slug=item_id)
            except Product.DoesNotExist:
                bag.pop(item_id)
                continue

            bag_items.append({
                'type': 'product',
                'product': product,
                'quantity': item,
                'bag_total': product.price * item
            })

            total_price += product.price * item
            total_bag_items += item

    context = {
        'total_price': total_price,
        'bag_items': bag_items,
        'total_bag_items': total_bag_items,
    }

    return context
