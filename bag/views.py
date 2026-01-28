from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product

# Create your views here.


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = int(request.POST.get('quantity', 1))

    bag = request.session.get('bag', {})

    product_id_as_str = str(product.id)

    if product_id_as_str in bag:
        bag[product_id_as_str] += quantity
    else:
        bag[product_id_as_str] = quantity

    request.session['bag'] = bag

    print(bag)

    return redirect('product_detail', slug=slug)
