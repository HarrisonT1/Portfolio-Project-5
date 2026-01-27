from django.shortcuts import render
from django.db.models import Q
from .models import SweetCategory, DietaryTag, Product

# Create your views here.


def all_products(request):
    products = Product.objects.all()

    query = None
    categories = None

    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    if 'category' in request.GET:
        categories = request.GET['category'].lower().split(',')
        products = products.filter(sweet_category__slug__in=categories)

    context = {
        'products': products,
        'search': query,
        'searched_categories': categories,
    }

    return render(request, 'products/product-list.html', context)
