from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product

# Create your views here.


def view_bag(request):
    bag = request.session.get('bag', {})
    bag_items = []

    total_price = 0

    for product_id, quantity in bag.items():
        product = get_object_or_404(Product, id=product_id)
        bag_items.append({
            'product': product,
            'quantity': quantity,
            'bag_total': product.price * quantity
        })

        total_price = product.price * quantity

    context = {
        'total_price': total_price,
        'bag_items': bag_items
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = request.POST.get('quantity', 1)

    bag = request.session.get('bag', {})

    if product.id in bag:
        bag[product.id] += quantity
    else:
        bag[product.id] = quantity

    request.session['bag'] = bag

    print(bag)

    return redirect('product_detail', slug=slug)
