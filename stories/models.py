from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from users.models import User

class Genre(models.Model):
    """Genre of the story"""

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Like(models.Model):
    """Likes on each Story"""

    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    likes = models.IntegerField(null=True)

    def __str__(self):
        return self.name.username


class Story(models.Model):
    """Class for any story published"""

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.author.username


class Comment(models.Model):
    """Class for comments to be posted on each story"""

    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]
