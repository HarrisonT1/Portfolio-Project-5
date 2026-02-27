# Standard libary imports
# Third-party imports
# Django imports
from django import forms
# Local imports
from .models import Order


class OrderForm(forms.ModelForm):
    """
    form for creating an order

    A save_info checkbox to save the info from the form
    """
    save_info = forms.BooleanField(
        required=False, label='Save information for your next order')

    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'phone_number',
            'country',
            'postcode',
            'city',
            'town',
            'street_address1',
            'street_address2',
        ]
        widgets = {
            'phone_number': forms.NumberInput(attrs={
                'min': 0
            })
        }
