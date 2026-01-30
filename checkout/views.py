from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm
from .models import OrderLineItem, Order
from products.models import Product

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

            for item_slug, quantity in bag.items():
                product = get_object_or_404(Product, slug=item_slug)
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    line_item_total=product.price * quantity
                )

            request.session['bag'] = {}
            return redirect(
                'checkout_success', order_number=order.order_number)
    else:
        form = OrderForm()

    bag_items = []
    subtotal = 0

    for item_slug, quantity in bag.items():
        product = get_object_or_404(Product, slug=item_slug)
        total = product.price * quantity
        subtotal += total
        bag_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    context = {
        'form': form,
        'quantity': bag_items,
        'subtotal': subtotal,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
