from django.shortcuts import render
from django.db.models.functions import Random
from reviews.models import Review

# Create your views here.


def home(request):
    reviews = Review.objects.filter(approved=True, rating__gte=4).order_by(Random())[:3]

    context = {
        'reviews': reviews,
    }

    return render(request, 'home/home.html', context)
