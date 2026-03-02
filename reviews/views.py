# Standard libary imports
# Third-party imports
# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# Local imports
from .forms import ReviewForm
from .models import Review

# Create your views here.


def review(request):
    """
    Allow authenticated users to submit a review

    Show success message
    """

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to make a review")
        return redirect('account_login')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.name = request.user.username
            review.save()
            messages.success(
                request,
                (f"Thank you {request.user.username}. Your review was"
                 "submitted, it will be reviewed by staff before being "
                 "approved, you can edit this review through your account"))
            return redirect('home')
    else:
        form = ReviewForm()

    context = {
        'form': form,
    }

    return render(request, 'reviews/reviews.html', context)


@login_required
def review_edit(request, review_id):
    """
    Allows a user to edit a review

    Editing resets approval status
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.approved = False
            form.save()
            messages.success(
                request,
                ('Your review has successfully been changed, if the review '
                 'was already approved, it will need reapproval'))
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
    """
    Allows a user to delete their review
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review was successfully deleted')
        return redirect('profile')

    return render(request, 'reviews/review_delete.html')


def review_list(request):
    """
    Renders a template showing all approved reviews
    """
    reviews = Review.objects.filter(approved=True)

    context = {
        'reviews': reviews,
    }

    return render(request, 'reviews/review_list.html', context)
