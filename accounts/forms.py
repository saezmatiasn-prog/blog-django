from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from config.forms import BootstrapFormMixin
from config.validators import TAMANO_MAXIMO_IMAGEN_MB, validar_tamano_imagen

from .models import Perfil


class RegistroForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class UsuarioForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
        }


class PerfilForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("avatar", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].validators.append(validar_tamano_imagen)
        self.fields["avatar"].help_text = f"Opcional. Hasta {TAMANO_MAXIMO_IMAGEN_MB} MB."
