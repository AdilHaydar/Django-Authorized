from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Post
from .forms import PostForm
from user.decorators import allowed_groups, allowed_perms

# Create your views here.

def view_post(request):
    posts = Post.objects.all()

    return render(request,'blog/view_blog.html',{'posts':posts})

@allowed_perms('add_post')
def add_post(request):

    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        created_post = form.save(commit=False)
        created_post.user = request.user
        created_post.save()

        return redirect(reverse('show_post', kwargs={'pk':created_post.id}))

    return render(request,'blog/add_post.html',{'form':form})


@allowed_perms('view_post')
def show_post(request, pk):

    post = Post.objects.get(id = pk)

    return render(request,'blog/show_post.html',{'post':post})

@allowed_perms('change_post')
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()

        return redirect(reverse('show_post', kwargs={'pk':pk}))
    return render(request,'blog/edit_post.html',{'form':form})


