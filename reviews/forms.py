# Standard libary imports
# Third-party imports
# Django imports
from django import forms
# Local imports
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_message']
        widgets = {
            'rating': forms.Select(),
            'review_message': forms.Textarea()
        }
