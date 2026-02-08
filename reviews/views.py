from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review

# Create your views here.


@login_required
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


@login_required
def review_list(request):
    reviews = Review.objects.filter(approved=True)

    context = {
        'reviews': reviews,
    }

    return render(request, 'reviews/review_list.html', context)
