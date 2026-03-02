# Standard libary imports
# Third-party imports
# Django imports
from django import forms
# Local imports
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    form for creating a review
    """
    class Meta:
        model = Review
        fields = ['rating', 'review_message']
        widgets = {
            'rating': forms.Select(),
            'review_message': forms.Textarea()
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise forms.ValidationError("Please select a star rating")
        return rating
