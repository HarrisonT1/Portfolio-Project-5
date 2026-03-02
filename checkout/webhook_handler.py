# Standard libary imports
import json
import time
# Third-party imports
import stripe
# Django imports
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
# Local imports
from .models import Order
from .utils import create_line_items
from accounts.models import UserAccount


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    # FROM CI BOUTIQUE ADO WALKTHROUGH
    def _send_confirmation_email(self, order):
        """ sends an email to the user on checkout """
        order.update_total()
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle stripe webhook events
        """
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
        save_info = metadata.get(
            'save_info', False)  # default False if missing
        username = metadata.get('username', 'AnonymousUser')
        email = metadata.get('meta', '')
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        if username != 'Guest':
            try:
                profile = UserAccount.objects.get(user__username=username)
            except UserAccount.DoesNotExist:
                profile = None

            if profile and save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_city = shipping_details.address.city
                profile.default_town = shipping_details.address.city
                profile.default_street_address1 = (
                    shipping_details.address.line1)
                profile.default_street_address2 = (
                    shipping_details.address.line2)
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        user=profile,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        city__iexact=shipping_details.address.city,
                        street_address1__iexact=shipping_details.address.line1,
                        street_address2__iexact=shipping_details.address.line2,
                        grand_total=grand_total,
                        stripe_pid=pid
                    )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f"Webhook received: {event['type']} | "
                         "SUCCESS: Verified order already in database"),
                status=200)
        else:
            order = None
            try:
                bag_data = json.loads(bag)
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    grand_total=grand_total,
                    stripe_pid=pid
                )
                create_line_items(bag_data, order=order)
                order.update_total()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f"Webhook received: {event["type"]}  | "
                     "SUCCESS: Verified order already in database"),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
