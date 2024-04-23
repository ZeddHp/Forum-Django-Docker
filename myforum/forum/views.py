from io import BytesIO
import os
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

from .forms import CommentForm, LoginForm, PostForm, SignupForm
from .models import Comment, Post


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


def post_list(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 5)  # Paginate with 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'posts.html', {'posts': posts})


# For file upload
def upload(request):
    if request.method == 'POST':
        if 'document' not in request.FILES:
            return HttpResponseBadRequest("Select file to upload.")
        uploaded_file = request.FILES['document']
        max_size = 5 * 1024 * 1024
        if uploaded_file.size > max_size:
            return HttpResponseBadRequest("File size exceeds the maximum allowed limit of 5 MB.")
        allowed_extensions = ['.pdf', '.txt', '.jpeg', '.jpg', '.png']
        ext = os.path.splitext(uploaded_file.name)[1]
        if ext.lower() not in allowed_extensions:
            return HttpResponseBadRequest("Unsupported file type. Only PDF, TXT, JPEG, JPG, and PNG files are allowed.")

        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(name)

        request.session['uploaded_file'] = name
        return redirect('view_files')
    return render(request, 'upload.html')


# For viewing uploaded files
def view_files(request):
    # Retrieve the uploaded file name from the session
    file_name = request.session.get('uploaded_file', '')

    # Path to the media folder
    media_path = settings.MEDIA_ROOT

    # Check if the media folder exists and if it contains any files
    if os.path.exists(media_path) and os.listdir(media_path):
        # Get a list of uploaded file names
        uploaded_files = os.listdir(media_path)
    else:
        # If media folder does not exist or is empty, set uploaded_files to an empty list
        uploaded_files = []

    # Clear the file_name session variable
    request.session['uploaded_file'] = None

    return render(request, 'view_files.html', {'uploaded_files': uploaded_files, 'file_name': file_name})


def generate_pdf(request):
    # Create an in-memory PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="posts.pdf"'

    # Create a buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Fetch posts from the database
    posts = Post.objects.all()

    # Define a style for the paragraph
    styles = getSampleStyleSheet()
    body_style = styles['BodyText']

    # Create a list to hold the paragraphs
    elements = []

    # Initialize post counter
    post_counter = 1

    # Iterate through each post
    for post in posts:
        # Add post number
        elements.append(Paragraph(f"<b>#{post_counter}</b>", body_style))
        elements.append(Paragraph("<br/>", body_style))  # Add some space

        # Add title, content, and author to the PDF
        elements.append(Paragraph(f"<b>Title:</b> {post.title}", body_style))
        elements.append(
            Paragraph(f"<b>Content:</b> {post.content}", body_style))
        elements.append(
            Paragraph(f"<b>Create at:</b> {post.created_at}", body_style))
        elements.append(Paragraph(f"<b>Author:</b> {post.author}", body_style))
        elements.append(Paragraph("<br/>", body_style))  # Add some space

        # Add divider between posts
        elements.append(Paragraph("-" * 50, body_style))
        elements.append(Paragraph("<br/>", body_style))  # Add some space

        # Increment post counter
        post_counter += 1

    # Build the PDF
    doc.build(elements)

    # Write the buffer to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def sanitize_content(content):
    # Remove any IP addresses
    sanitized_content = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '', content)
    return sanitized_content
