from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistroForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "accounts/registro.html"
    success_url = reverse_lazy("posts:post_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("posts:post_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"¡Bienvenido/a, {self.object.username}! Tu cuenta se creó correctamente.")
        return response
