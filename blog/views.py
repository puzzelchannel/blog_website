import os
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import NewPostForm
from .models import Post

os.system('clear')


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status='pub')
    context = {
        'posts': posts,
    }
    return render(request, template_name='blog/post_list.html', context=context)


def post_detail(request, id):
    post_detail = get_object_or_404(Post, id=id)
    context = {
        'posts_detail': post_detail,
    }
    return render(request, template_name='blog/post_detail.html', context=context)


def create_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts_list')

    else:
        form = NewPostForm()

    context = {
        'create_post_form': form,
    }
    return render(request, template_name='blog/post_create.html', context=context)
