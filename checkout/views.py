from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .forms import OrderForm
from .models import Order
from .utils import calc_delivery_cost, create_line_items, create_order, stripe_payment_intent

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
        form = OrderForm()

        bag = request.session.get('bag', {})

        if not bag:
            return redirect('products')

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
