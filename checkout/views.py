from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm
from .models import OrderLineItem, Order
from products.models import Product
from django.conf import settings

# Create your views here.


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        return redirect('products')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            for item_slug, item_data in bag.items():
                if not isinstance(item_data, int):
                    continue
                product = get_object_or_404(Product, slug=item_slug)
                quantity = item_data
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    line_item_total=product.price * quantity
                )

            order.create_total()

            request.session['bag'] = {}
            return redirect(
                'checkout_success', order_number=order.order_number)
    else:
        form = OrderForm()

    bag_items = []
    order_total = 0

    for item_slug, item_data in bag.items():
        if not isinstance(item_data, int):
            continue
        quantity = item_data
        product = get_object_or_404(Product, slug=item_slug)
        line_total = product.price * quantity
        order_total += line_total

        bag_items.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total
        })

    delivery_method = request.POST.get('delivery_method')

    if order_total >= settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = 0
    else:
        if delivery_method == 'premium':
            delivery_cost = settings.PREMIUM_DELIVERY_COST
        else:
            delivery_cost = settings.STANDARD_DELIVERY_COST

        grand_total = order_total + delivery_cost

    context = {
        'form': form,
        'quantity': bag_items,
        'order_total': order_total,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
        'FREE_DELIVERY_THRESHOLD': settings.FREE_DELIVERY_THRESHOLD,
        'STANDARD_DELIVERY_COST': settings.STANDARD_DELIVERY_COST,
        'PREMIUM_DELIVERY_COST': settings.PREMIUM_DELIVERY_COST,
        'stripe_public_key': 'pk_test_51Sp6zII10BMycAneUF1SzLC5123VXXviT4RGzsg2sDdlwpIuaGGOVY9nivnH7edlSHxYo078MvSSJxtCFQUuWOyp00V50a910Y',
        'client_secret': 'test_key',
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
