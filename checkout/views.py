from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import stripe
import json
from .forms import OrderForm
from .models import Order
from .utils import calc_delivery_cost, create_line_items, create_order, stripe_payment_intent
from accounts.models import UserAccount

# Create your views here.


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    delivery_method = request.POST.get('delivery_method', 'standard')

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        if not bag:
            return redirect('products')

        form = OrderForm(request.POST)
        if form.is_valid():
            order = create_order(form, request.user)

            if request.user.is_authenticated:
                account, _ = UserAccount.objects.get_or_create(user=request.user)
                order.user = account

            order.delivery_method = delivery_method
            order.save()

            create_line_items(bag, order=order)

            if request.user.is_authenticated and form.cleaned_data.get('save_info'):
                account, _ = UserAccount.objects.get_or_create(user=request.user)

                account.default_full_name = order.full_name
                account.default_email = order.email
                account.default_phone_number = order.phone_number
                account.default_country = order.country
                account.default_postcode = order.postcode
                account.default_city = order.city
                account.default_town = order.town
                account.default_street_address1 = order.street_address1
                account.default_street_address2 = order.street_address2

                account.save()

            request.session['bag'] = {}

            return redirect('checkout_success', order_number=order.order_number)
    else:
        bag = request.session.get('bag', {})

        if not bag:
            return redirect('products')

        form = OrderForm()

        if request.user.is_authenticated:
            account, _ = UserAccount.objects.get_or_create(user=request.user)
            form = OrderForm(initial={
                'full_name': account.default_full_name,
                'email': account.default_email,
                'phone_number': account.default_phone_number,
                'country': account.default_country,
                'postcode': account.default_postcode,
                'city': account.default_city,
                'town': account.default_town,
                'street_address1': account.default_street_address1,
                'street_address2': account.default_street_address2,
            })

        bag_items, order_total = create_line_items(bag)

        delivery_cost = calc_delivery_cost(order_total, delivery_method)
        grand_total = order_total + delivery_cost
        intent = stripe_payment_intent(grand_total, stripe_secret_key)

        free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD

        if order_total < free_delivery_threshold:
            amount_needed_for_free_delivery = free_delivery_threshold - order_total
        else:
            amount_needed_for_free_delivery = 0

        context = {
            'form': form,
            'bag_items': bag_items,
            'order_total': order_total,
            'delivery_cost': delivery_cost,
            'grand_total': grand_total,
            'FREE_DELIVERY_THRESHOLD': settings.FREE_DELIVERY_THRESHOLD,
            'STANDARD_DELIVERY_COST': settings.STANDARD_DELIVERY_COST,
            'PREMIUM_DELIVERY_COST': settings.PREMIUM_DELIVERY_COST,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'delivery_method': delivery_method,
            'amount_needed_for_free_delivery': amount_needed_for_free_delivery
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    bag_items = order.lineitems.all()

    for item in bag_items:
        if item.product:
            item.line_total = item.product.price * item.quantity
        else:
            item.line_total = 0

    product_items = bag_items.filter(product__isnull=False).exists()
    pick_and_mix_items = bag_items.filter(pick_and_mix_bag__isnull=False).exists()

    context = {
        'order': order,
        'bag_items': bag_items,
        'product_items': product_items,
        'pick_and_mix_items': pick_and_mix_items,
    }

    return render(request, 'checkout/checkout_success.html', context)


@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            return HttpResponse('Missing client secret', status=400)

        pid = client_secret.split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'username': request.user.username if request.user.is_authenticated else 'Anonymous',
        })
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(content=str(e), status=400)
