from django.shortcuts import render
from django.db.models import Q
from .models import SweetCategory, DietaryTag, Product

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    categories = SweetCategory.objects.all()
    dietary_tags = DietaryTag.objects.all()

    selected_dietary_tags = []
    query = None
    search_categories = None

    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    if 'category' in request.GET:
        search_categories = request.GET['category'].lower().split(',')
        products = products.filter(
            sweet_category__slug__in=search_categories).distinct()

    if 'dietary_tag' in request.GET:
        selected_dietary_tags = request.GET.getlist('dietary_tag')
        products = products.filter(
            dietary_tags__slug__in=selected_dietary_tags).distinct()

    context = {
        'dietary_tags': dietary_tags,
        'products': products,
        'search': query,
        'searched_categories': search_categories,
        'categories': categories,
        'selected_dietary_tags': selected_dietary_tags,
    }

    return render(request, 'products/product-list.html', context)
