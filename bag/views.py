from django.shortcuts import render, get_object_or_404, redirect
import uuid
from products.models import Product
from pick_and_mix.models import PickAndMixBag

# Create your views here.


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_slug = product.slug
    quantity = int(request.POST.get('quantity', 1))

    bag = request.session.get('bag', {})

    if product_slug in bag:
        bag[product_slug] += quantity
    else:
        bag[product_slug] = quantity

    request.session['bag'] = bag

    print(bag)

    return redirect('product_detail', slug=slug)


def pick_and_mix_add_basket(request, bag_slug):

    pick_and_mix = request.session.get('pick_and_mix')
    bag = request.session.get('bag', {})
    pnmbag = get_object_or_404(PickAndMixBag, slug=bag_slug)
    unique_bag_id = f"pick_and_mix_{pnmbag.slug}_{uuid.uuid4().hex}"
    print(unique_bag_id)    

    bag[unique_bag_id] = {
        'quantity': 1,
        'price': pnmbag.price,
        'pick_and_mix': pick_and_mix,
    }

    request.session['bag'] = bag

    request.session.pop('pick_and_mix', None)

    return redirect('view_bag')


def remove_from_bag(request, slug):
    bag = request.session.get('bag', {})
    bag.pop(slug, None)
    request.session['bag'] = bag

    return redirect('view_bag')


def adjust_bag(request, slug):
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity'))

    if quantity > 0:
        bag[slug] = quantity
    else:
        bag.pop(slug, None)

    request.session['bag'] = bag
    return redirect('view_bag')
