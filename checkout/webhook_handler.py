from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
import time
import stripe
from .models import Order, OrderLineItem
from products.models import Product
from pick_and_mix.models import PickAndMixBag
from accounts.models import UserAccount


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    # Template for boutique ado walkthrough
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id

        metadata = intent.metadata or {}
        bag = metadata.get('bag', '{}')
        save_info = metadata.get('save_info', False)  # default False if missing
        delivery_method = metadata.get('delivery_method', 'standard')
        username = metadata.get('username', 'AnonymousUser')

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        email = metadata.get('email', '')
        delivery_method = intent.metadata.get('delivery_method')

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            profile = UserAccount.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_city = shipping_details.address.city
                profile.default_town = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        user=profile,
                        email=email,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        city__iexact=shipping_details.address.city,
                        town__iexact=shipping_details.address.city,
                        street_address1__iexact=shipping_details.address.line1,
                        street_address2__iexact=shipping_details.address.line2,
                        delivery_method=delivery_method,
                        grand_total=grand_total,
                        stripe_pid=pid
                    )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        city=shipping_details.address.city,
                        town=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        delivery_method=delivery_method,
                        grand_total=grand_total,
                        stripe_pid=pid
                    )
                except Exception as e:
                    print("order creation failed", e)
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(slug=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                print("Webhook ERROR:", e)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}  | SUCCESS: Verified order already in database',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
