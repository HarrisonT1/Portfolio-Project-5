from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
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
        pid = intent.id

        if Order.objects.filter(stripe_pid=pid).exists():
            return HttpResponse(
                content=f'Webhook Recieved: {event["type"]} | Order already exists',
                status=200
            )
        try:
            bag = json.loads(intent.metadata.bag)
            shipping_details = json.loads(intent.metadata.shipping)
        except (AttributeError, json.JSONDecodeError):
            return HttpResponse(
                content='Webhook error: Invalid metadata',
                status=400)
        try:
            order = Order.objects.create(
                stripe_pid=pid,
                full_name=shipping_details.get('name'),
                email=shipping_details.get('email'),
                phone=shipping_details.get('phone'),
                country=shipping_details.get('country'),
                postal_code=shipping_details.get('postal_code'),
                city=shipping_details.get('city'),
                line1=shipping_details.get('line1'),
                line2=shipping_details.get('line2'),
            )

            for item_slug, item_data in bag.items():
                # regular items
                if isinstance(item_data, int):
                    product = get_object_or_404(Product, slug=item_slug)

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
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order created',
                status=200
            )
        except Exception as e:
            if 'order' in locals():
                order.delete()
            return HttpResponse(
                content=f'Webhook Error: {str(e)}',
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
