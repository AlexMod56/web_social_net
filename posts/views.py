from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm

@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-list')
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)  # Убираем лайк, если он уже был

    else:
        post.liked_by.add(request.user)  # Добавляем лайк

    return redirect('post-detail', pk=post.pk)