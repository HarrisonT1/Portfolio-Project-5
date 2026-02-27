# Standard libary imports
# Third-party imports
# Django imports
from django import forms
# Local imports
from .models import UserAccount


class UserAccountForm(forms.ModelForm):
    """
    Form for updating a user's contact and default address information
    """
    class Meta:
        model = UserAccount
        fields = (
            'default_full_name',
            'default_email',
            'default_phone_number',
            'default_country',
            'default_postcode',
            'default_city',
            'default_town',
            'default_street_address1',
            'default_street_address2',
        )
        labels = {
            'default_full_name': 'Full name',
            'default_email': 'Email',
            'default_phone_number': 'Phone number',
            'default_country': 'Country',
            'default_postcode': 'Postcode',
            'default_city': 'City',
            'default_town': 'Town',
            'default_street_address1': 'Street address 1',
            'default_street_address2': 'Street address 2',
        }
