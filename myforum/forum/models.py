from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(validators=[MaxLengthValidator(1000)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[MaxLengthValidator(1000)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
