from django.shortcuts import render
from .models import PickAndMixBag

# Create your views here.


def pick_and_mix(request):
    pnmbag = PickAndMixBag.objects.all()

    context = {
        'pnmbag': pnmbag,
    }

    return render(request, 'pick_and_mix/pick-and-mix.html', context)
