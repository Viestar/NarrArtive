from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Representation of the user """
    # name = models.CharField(max_length=200, null=True)
    # email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    #
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []


class Topic(models.Model):
    """ Representation of the story topics """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    """ Class to represent the story telling room """
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.host


class Message(models.Model):
    """ Representation of the comment/message class """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
