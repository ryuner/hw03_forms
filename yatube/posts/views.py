from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    post_counter = post_list.count()
    page_obj = paginator.get_page(page_number)
    context = {
        'user_profile': author,
        'page_obj': page_obj,
        'post_counter': post_counter
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    author_posts_count = post.author.posts.count()
    context = {
        'post': post,
        'author_posts_count': author_posts_count
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html',
                               {'form': form, 'is_edit': True,
                                'post_id': post_id})
    form = PostForm(instance=post)

    return render(request, 'posts/create_post.html',
                           {'form': form, 'is_edit': True, 'post_id': post_id})
