from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
import time
import stripe
from .models import Order, OrderLineItem
from products.models import Product
from pick_and_mix.models import PickAndMixBag


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        intent = event.data.object
        print(intent)
        pid = intent.id
        bag = intent.metadata.bag
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        amount = intent.charges.data[0].amount
        grand_total = round(amount / 100, 2)

        bag_str = intent.metadata.get('bag', '{}')
        try:
            bag = json.loads(bag_str)
        except json.JSONDecodeError:
            bag = {}

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 0
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postal_code,
                    city__iexact=shipping_details.city,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    grand_total=grand_total,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content='Webhook received: Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    stripe_pid=pid,
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone=shipping_details.phone,
                    country=shipping_details.country,
                    postcode=shipping_details.postal_code,
                    city=shipping_details.city,
                    street_address1=shipping_details.line1,
                    street_address2=shipping_details.line2,
                    grand_total=grand_total,
                )
                for item_id, item_data in bag.items():
                    # regular items
                    if isinstance(item_data, int):
                        product = get_object_or_404(Product, id=item_id)

                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    # pick and mix items
                    elif isinstance(item_data, dict) and 'pick_and_mix' in item_data:
                        pnm_data = item_data['pick_and_mix']
                        pnmbag = get_object_or_404(PickAndMixBag, slug=pnm_data['bag_slug'])

                        OrderLineItem.objects.create(
                            order=order,
                            pick_and_mix_bag=pnmbag,
                            quantity=1
                        )
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: error: {e}',
                    status=500
                )
        return HttpResponse(
            content='Webhook received: created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
