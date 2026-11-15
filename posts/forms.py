from django import forms

from config.forms import BootstrapFormMixin
from config.validators import TAMANO_MAXIMO_IMAGEN_MB, validar_tamano_imagen

from .models import Post


class PostForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen"]
        widgets = {
            "contenido": forms.Textarea(attrs={"rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["imagen"].validators.append(validar_tamano_imagen)
        self.fields["imagen"].help_text = f"Opcional. Hasta {TAMANO_MAXIMO_IMAGEN_MB} MB."
