from django import forms

from config.forms import BootstrapFormMixin

from .models import Post


class PostForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={"rows": 10}),
        }
