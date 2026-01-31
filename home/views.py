from django.shortcuts import render
from reviews.models import Review

# Create your views here.


def home(request):
    reviews = Review.objects.filter(approved=True)

    context = {
        'reviews': reviews,
    }

    return render(request, 'home/home.html', context)
