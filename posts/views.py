from django.views.generic import DetailView, ListView

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
