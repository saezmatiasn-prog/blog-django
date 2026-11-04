from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


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


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["perfil"], _ = Perfil.objects.get_or_create(usuario=self.request.user)
        context["mis_posts"] = self.request.user.posts.all()
        return context


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Tu perfil se actualizó correctamente.")
            return redirect("accounts:perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    return render(
        request,
        "accounts/perfil_form.html",
        {"usuario_form": usuario_form, "perfil_form": perfil_form},
    )
