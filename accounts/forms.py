from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from config.forms import BootstrapFormMixin


class RegistroForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
