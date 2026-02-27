# Standard libary imports
# Third-party imports
# Django imports
from django.db.models.functions import Random
from django.shortcuts import render
# Local imports
from reviews.models import Review

# Create your views here.


def home(request):
    """
    Renders reviews on the home page

    renders the home template
    """
    reviews = Review.objects.filter(
        approved=True, rating__gte=4).order_by(Random())[:3]

    context = {
        'reviews': reviews,
    }

    return render(request, 'home/home.html', context)


def privacy_policy(request):
    """
    Renders privacy policy
    """
    return render(request, 'privacy_policy.html')
