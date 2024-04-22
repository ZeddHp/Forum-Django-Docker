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
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
import re


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
            # Sanitize the input
            sanitized_content = sanitize_content(form.cleaned_data['content'])

            post = form.save(commit=False)
            post.content = sanitized_content
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
        max_size = 5 * 1024 * 1024  # 5 MB in bytes
        if uploaded_file.size > max_size:
            return HttpResponseBadRequest("File size exceeds the maximum allowed limit of 5 MB.")
        allowed_extensions = ['.pdf', '.txt', '.jpeg', '.jpg', '.png']
        ext = os.path.splitext(uploaded_file.name)[1]
        if ext.lower() not in allowed_extensions:
            return HttpResponseBadRequest("Unsupported file type. Only PDF, TXT, JPEG, JPG, and PNG files are allowed.")

        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        return redirect('view_files')
    return render(request, 'upload.html', context)


# For viewing uploaded files
def view_files(request):
    uploaded_files = default_storage.listdir('')[1]
    return render(request, 'view_files.html', {'uploaded_files': uploaded_files})



def generate_pdf(request):
    # Create an HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="posts.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Start with a Y position for the first post. Adjust as necessary.
    y_position = 800
    line_height = 15

    # Fetch posts from the database
    posts = Post.objects.all()

    for post in posts:
        # For each post, draw the title and content on the PDF.
        p.drawString(100, y_position, f"Title: {post.title}")
        y_position -= line_height
        p.drawString(100, y_position, f"Content: {post.content}")
        y_position -= line_height
        p.drawString(100, y_position, f"Author: {post.author}")
        y_position -= (line_height * 2)  # Add extra space before the next post

        # Check if we need to start a new page.
        if y_position < 100:  # This threshold may need adjustment
            p.showPage()
            y_position = 800  # Reset Y position for the new page

    p.showPage()
    p.save()
    return response


def sanitize_content(content):
    # Remove any IP addresses
    sanitized_content = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '', content)
    return sanitized_content
