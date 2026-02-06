from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from decimal import Decimal
import stripe
from .models import OrderLineItem
from products.models import Product
from pick_and_mix.models import PickAndMixBag


def calc_delivery_cost(order_total, delivery_method='standard'):
    if order_total >= settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        if delivery_method == 'premium':
            delivery_cost = settings.PREMIUM_DELIVERY_COST
        else:
            delivery_cost = settings.STANDARD_DELIVERY_COST
    return delivery_cost


def create_line_items(bag, order=None):
    bag_items = []
    order_total = Decimal('0.00')

    if not bag:
        return redirect('products')

    for item_slug, item_data in bag.items():
        # regular items
        if isinstance(item_data, int):
            quantity = item_data
            product = get_object_or_404(Product, slug=item_slug)
            line_total = product.price * quantity
            order_total += line_total

            bag_items.append({
                'product': product,
                'quantity': quantity,
                'line_total': line_total
            })

            if order:
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
        # pick and mix items
        elif isinstance(item_data, dict) and 'pick_and_mix' in item_data:
            pnm_items = item_data['pick_and_mix']
            bag_slug = pnm_items['bag_slug']
            pnmbag = get_object_or_404(PickAndMixBag, slug=bag_slug)

            quantity = item_data.get('quantity', 1)
            bag_total = pnmbag.price * quantity

            order_total += bag_total

            bag_items.append({
                'pick_and_mix_bag': pnmbag,
                'quantity': 1,
                'line_total': bag_total,
            })

            if order:
                OrderLineItem.objects.create(
                    order=order,
                    product=None,
                    quantity=1,
                    line_item_total=bag_total,
                    pick_and_mix_bag=pnmbag,
                )

    return bag_items, order_total


def create_order(form):
    order = form.save(commit=False)
    order.save()
    return order


def stripe_payment_intent(grand_total, stripe_secret_key):
    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)
    return intent
