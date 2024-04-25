from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import generate_pdf, post_list

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload, name="upload"),
    path('view_files/', views.view_files, name='view_files'),
    path('posts/', post_list, name='post_list'),
    path('posts/page/<int:page>/', post_list, name='post_list_paginated'),
    path('posts/', views.posts, name='posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_comment/<int:post_id>/',
         views.add_comment, name='add_comment'),
    path('posts/pdf/', generate_pdf, name='posts_pdf')
]

# Define custom handler404 to render a specific template for 404 errors
handler404 = 'forum.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
