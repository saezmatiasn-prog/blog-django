from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.select_related("autor")


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.select_related("autor")


class AutorRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Exige sesión iniciada y que el usuario sea el autor del post."""

    def test_func(self):
        return self.get_object().autor == self.request.user


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_message = "El post se publicó correctamente."

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(AutorRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_message = "El post se actualizó correctamente."


class PostDeleteView(AutorRequeridoMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:post_list")
    success_message = "El post se eliminó correctamente."
