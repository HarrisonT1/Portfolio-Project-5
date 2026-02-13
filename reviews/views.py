from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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
            review.user = request.user
            review.name = request.user.username
            review.save()
            messages.success(request, f'Thank you {request.user.username}. Your reviews was submitted, it will be reviewed by staff before being approved, you can edit this review through your account')
            return redirect('home')
    else:
        form = ReviewForm()

    context = {
        'form': form,
    }

    return render(request, 'reviews/reviews.html', context)


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has successfully been changed, if the review was already approved, it will need reapproval')
            return redirect('profile')
        else:
            messages.error(request, 'The form is incorrect, please try again')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form
    }

    return render(request, 'reviews/reviews.html', context)


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review was successfully deleted')
        return redirect('profile')

    return render(request, 'reviews/review_delete.html')


@login_required
def review_list(request):
    reviews = Review.objects.filter(approved=True)

    context = {
        'reviews': reviews,
    }

    return render(request, 'reviews/review_list.html', context)
