from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post_detail'


class PostCreateView(generic.CreateView):
    template_name = 'blog/post_create.html'
    form_class = PostForm


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts_list')
