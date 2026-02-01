from django.shortcuts import render

# Create your views here.


def pick_and_mix(request):
    return render(request, 'pick_and_mix/pick-and-mix.html')
