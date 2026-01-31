from django.shortcuts import render, redirect
from .forms import ReviewForm

# Create your views here.


def review(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()

    context = {
        'form': form
    }

    return render(request, 'reviews/reviews.html', context)
