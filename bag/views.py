# Standard libary imports
import uuid
# Third-party imports
# Django imports
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
# Local imports
from .utils import get_bag_quantity
from pick_and_mix.models import PickAndMixBag
from products.models import Product

# Create your views here.


def view_bag(request):
    """
    Render bag template
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, slug):
    """
    Adds a product to the session bag

    Validates if stock is less than the user adds

    Displays a message
    """
    product = get_object_or_404(Product, slug=slug)
    product_slug = product.slug
    redirect_url = request.POST.get('redirect_url')

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    bag = request.session.get('bag', {})
    current_quantity = bag.get(product_slug, 0)
    reserved = get_bag_quantity(request, product_slug)

    if reserved + quantity > product.stock_level:
        messages.error(
            request, "Sorry, there is only"
            f" {product.stock_level} of {product.name} "
            "available. You already have them in your bag")
        return redirect(redirect_url)

    bag[product_slug] = current_quantity + quantity
    request.session['bag'] = bag

    messages.success(
        request, "Item successfully added to bag", extra_tags='bag')
    return redirect(redirect_url)


def pick_and_mix_add_basket(request, bag_slug):
    """
    Adds a pick and mix bag to the session bag

    stores the bag price and selected items

    Displays a message
    """
    pick_and_mix = request.session.get('pick_and_mix')
    bag = request.session.get('bag', {})
    pnmbag = get_object_or_404(PickAndMixBag, slug=bag_slug)
    unique_bag_id = f"pick_and_mix_{pnmbag.slug}_{uuid.uuid4().hex}"

    bag[unique_bag_id] = {
        'quantity': 1,
        'price': float(pnmbag.price),
        'pick_and_mix': {
            'bag_slug': pnmbag.slug,
            'items': pick_and_mix.get('items', {}),
        }
    }

    request.session['bag'] = bag
    request.session.pop('pick_and_mix', None)
    messages.success(
        request, "Item successfully added to bag", extra_tags='bag')

    return redirect('view_bag')


def remove_from_bag(request, slug):
    """
    Removes an item from the bag

    Displays a message
    """
    bag = request.session.get('bag', {})
    bag.pop(slug, None)
    request.session['bag'] = bag

    messages.success(request, "Item successfully removed from bag")
    return redirect('view_bag')


def adjust_bag(request, slug):
    """
    Allows the user to update the quantity of a product within the bag

    Validates if stock is less than the user adjusts to

    Displays a message
    """
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, slug=slug)
    redirect_url = request.POST.get('redirect_url')

    if quantity > product.stock_level:
        messages.error(
            request, "Sorry, there is only"
            f" {product.stock_level} of {product.name} "
            "available. You already have them in your bag")
        return redirect(redirect_url)

    if quantity > 0:
        bag[slug] = quantity
    else:
        bag.pop(slug, None)

    messages.success(request, "Item successfully adjusted")
    request.session['bag'] = bag
    return redirect('view_bag')
