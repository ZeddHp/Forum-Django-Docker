from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.core.files.storage import default_storage
import os

def index(request):
    return redirect('login')


def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})


##########################
# authentification views #
##########################
# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('posts')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


##############
# post views #
##############
# add post page
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})


# add comment page
@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Set the post for the comment
            comment.author = request.user
            comment.save()
            # Redirect back to the posts page
            return redirect('posts')
    else:
        form = CommentForm()  # Create a new form instance
    # Pass the form to the template context along with the post_id
    return render(request, 'add_comment.html', {'form': form, 'post_id': post_id})

# For file upload
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        allowed_extensions = ['.pdf', '.txt', '.jpeg', '.jpg', '.png']
        ext = os.path.splitext(uploaded_file.name)[1]
        if ext.lower() not in allowed_extensions:
            return HttpResponseBadRequest("Unsupported file type. Only PDF, TXT, JPEG, JPG, and PNG files are allowed.")
        
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'view_files.html', context)

# For viewing uploaded files
def view_files(request):
    uploaded_files = default_storage.listdir('')[1]
    return render(request, 'view_files.html', {'uploaded_files': uploaded_files})
