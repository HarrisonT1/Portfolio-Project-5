from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import PickAndMixBag
from products.models import Product, SweetCategory, DietaryTag

# Create your views here.


def pick_and_mix(request):
    pnmbag = PickAndMixBag.objects.all().order_by('price')

    context = {
        'pnmbag': pnmbag,
    }

    return render(request, 'pick_and_mix/pick-and-mix.html', context)


def pick_and_mix_products(request, slug):
    pnmbag = get_object_or_404(PickAndMixBag, slug=slug)

    session_bag = request.session.get('pick_and_mix')

    if session_bag and session_bag.get('bag_id') != pnmbag.id:
        del request.session['pick_and_mix']
        session_bag = None
        messages.warning(request, "Your previous pick and mix bag was cleared because you selected a different size")

    if not session_bag:
        request.session['pick_and_mix'] = {
            'bag_id': pnmbag.id,
            'bag_slug': pnmbag.slug,
            'max_weight': pnmbag.max_weight_in_grams,
            'total_weight': 0,
            'items': {},
        }
        messages.info(request, f"You've Started a new {pnmbag.name} pick and mix bag")
        session_bag = request.session['pick_and_mix']

    for slug_key, item in session_bag.get('items', {}).items():
        try:
            product = Product.objects.get(slug=slug_key)
            item['name'] = product.name
        except Product.DoesNotExist:
            item['name'] = slug_key

    products = Product.objects.exclude(sweet_category__slug='boxes-gifts')
    categories = SweetCategory.objects.exclude(slug="boxes-gifts")
    dietary_tags = DietaryTag.objects.all()

    selected_dietary_tags = []
    selected_category = []
    query = None

    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    if 'category' in request.GET:
        selected_category = request.GET.getlist('category')
        products = products.filter(
            sweet_category__slug__in=selected_category).distinct()

    if 'dietary_tag' in request.GET:
        selected_dietary_tags = request.GET.getlist('dietary_tag')
        products = products.filter(
            dietary_tag__slug__in=selected_dietary_tags).distinct()

    context = {
        'pnmbag': pnmbag,
        'dietary_tags': dietary_tags,
        'products': products,
        'search': query,
        'categories': categories,
        'selected_dietary_tags': selected_dietary_tags,
        'selected_category': selected_category,
        'pick_and_mix': session_bag,
    }

    return render(request, 'pick_and_mix/pick-and-mix-list.html', context)


def pick_and_mix_add(request, bag_slug, product_slug):
    pnmbag = get_object_or_404(PickAndMixBag, slug=bag_slug)
    product = get_object_or_404(Product, slug=product_slug)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    pick_and_mix = request.session.get('pick_and_mix', {
        'bag_id': pnmbag.id,
        'max_weight': pnmbag.max_weight_in_grams,
        'items': {},
        'total_weight': 0,
    })

    sweet_category_weight = product.sweet_category.weight_in_grams
    total_sweet_category_weight = product.sweet_category.weight_in_grams * quantity
    new_bag_weight = pick_and_mix['total_weight'] + total_sweet_category_weight

    if new_bag_weight > pick_and_mix['max_weight']:
        messages.warning(request, "That would exceed your bag's weight limit.")
        return redirect('pick_and_mix_products', slug=bag_slug)

    item = pick_and_mix['items'].get(product.slug)

    current_quantity = item['quantity'] if item else 0
    new_total = current_quantity + quantity

    if new_total > product.stock_level:
        messages.error(request, f'There is no remaining stock of {product.name}')
        return redirect('pick_and_mix_products', slug=bag_slug)

    if item:
        item['quantity'] += quantity
        item['total_weight'] += total_sweet_category_weight
    else:
        pick_and_mix['items'][product.slug] = {
            'quantity': quantity,
            'weight': sweet_category_weight,
            'total_weight': total_sweet_category_weight,
        }

    pick_and_mix['total_weight'] = new_bag_weight
    request.session['pick_and_mix'] = pick_and_mix
    messages.success(request, "Item successfully added to pick and mix bag", extra_tags='pick_and_mix_bag')
    print(pick_and_mix)

    return redirect('pick_and_mix_products', slug=bag_slug)
