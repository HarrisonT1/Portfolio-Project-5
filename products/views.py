from django.shortcuts import render
from django.db.models import Q
from .models import SweetCategory, DietaryTag, Product

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    categories = SweetCategory.objects.all()

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
        products = products.filter(sweet_category__slug__in=search_categories)

    context = {
        'products': products,
        'search': query,
        'searched_categories': search_categories,
        'categories': categories,
    }

    return render(request, 'products/product-list.html', context)
