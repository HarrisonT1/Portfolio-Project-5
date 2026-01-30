from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import SweetCategory, DietaryTag, Product

# Create your views here.


def all_products(request):
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
        'dietary_tags': dietary_tags,
        'products': products,
        'search': query,
        'categories': categories,
        'selected_dietary_tags': selected_dietary_tags,
        'selected_category': selected_category,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
