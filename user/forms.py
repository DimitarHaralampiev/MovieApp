from django import forms
from django.contrib.auth.models import User

from .models import LocationUser, UserProfile


class UserForm(forms.ModelForm):
    """
    Form for updating user details.

    Meta:
    - model: User: The User model.
    - fields: Tuple of fields to include in the form.
    """
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile details.

    Meta:
    - model: UserProfile: The UserProfile model.
    - fields: Tuple of fields to include in the form.
    """
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'photo_profile', )


class UserLocationForm(forms.ModelForm):
    """
    Form for updating user location details.

    Meta:
    - model: LocationUser: The LocationUser model.
    - fields: Set of fields to include in the form.
    """
    address_1 = forms.CharField(required=True)

    class Meta:
        model = LocationUser
        fields = {'address_1', 'address_2', 'city', }