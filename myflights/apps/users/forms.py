from django.contrib.auth import forms
from django.forms import EmailField

from .models import User


class UserCreationForm(forms.UserCreationForm):
    """Provides functionality to create new user from admin site.
    """

    class Meta:
        model = User
        fields = ('email',)
        field_classes = {'email': EmailField}


class UserChangeForm(forms.UserChangeForm):
    """Provides functionality to change user from admin site.
    """

    class Meta:
        model = User
        fields = ('email',)
        field_classes = {'email': EmailField}
