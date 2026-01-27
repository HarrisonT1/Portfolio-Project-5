from django.shortcuts import render
from django.db.models import Q
from .models import SweetCategory, DietaryTag, Product

# Create your views here.


def all_products(request):
    products = Product.objects.all()

    query = None

    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    context = {
        'products': products,
        'search': query,
    }

    return render(request, 'products/product-list.html', context)
