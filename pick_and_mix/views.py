from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import PickAndMixBag
from products.models import Product, SweetCategory, DietaryTag

# Create your views here.


def pick_and_mix(request):
    pnmbag = PickAndMixBag.objects.all()

    context = {
        'pnmbag': pnmbag,
    }

    return render(request, 'pick_and_mix/pick-and-mix.html', context)


def pick_and_mix_products(request, slug):
    pnmbag = get_object_or_404(PickAndMixBag, slug=slug)

    products = Product.objects.all()
    categories = SweetCategory.objects.all()
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
    }

    return render(request, 'pick_and_mix/pick-and-mix-list.html', context)


def pick_and_mix_add(request, bag_slug, product_slug):
    pnmbag = get_object_or_404(PickAndMixBag, slug=bag_slug)
    product = get_object_or_404(Product, slug=product_slug)

    quantity = int(request.POST.get('quantity', 1))

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
        return redirect('pick_and_mix_products', slug=bag_slug)

    item = pick_and_mix['items'].get(product.slug)

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

    print(pick_and_mix)

    return redirect('pick_and_mix_products', slug=bag_slug)
