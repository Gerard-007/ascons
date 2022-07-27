from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password")
        model = User


class UserChangeForm(UserChangeForm):

    class Meta:
        fields = (
            "avatar",
            "bio",
            "phone",
            'gender',
            'fname',
            'lname',
            'business_name',
            'number_of_workers',
            'business_address',
            'business_state',
            'business_country',
        )
        model = User