from django import forms
from .models import UserAccount


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = (
            'default_full_name'
            'default_email'
            'default_phone_number'
            'default_country'
            'default_postcode'
            'default_city'
            'default_town'
            'default_street_address1'
            'default_street_address2'
        )
