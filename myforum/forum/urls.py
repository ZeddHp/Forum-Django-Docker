from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload, name="upload" ),
    path('posts/', views.posts, name='posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_comment/<int:post_id>/',
         views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)