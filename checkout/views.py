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
            order = create_order(form)
            order.delivery_method = delivery_method
            order.save(update_fields=['delivery_method'])

            create_line_items(bag, order=order)

            order.update_total()

            request.session['bag'] = {}

            return redirect('checkout_success', order_number=order.order_number)
    else:
        bag = request.session.get('bag', {})

        if not bag:
            return redirect('products')

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
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(content=e, status=400)
