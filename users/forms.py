from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    """ Form to use by user signing up"""
    class Meta:
        model = User
        fields = ['username', 'email']
        # fields = '__all__'


class RoomForm(ModelForm):
    """ Form to be used by users to create stories """
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants', 'host', 'age', 'country']


class MessageForm(ModelForm):
    """ Form to used by users to create comments/messages """
    class Meta:
        model = Message
        fields = '__all__'


class UserForm(ModelForm):
    """ Form to be used by users in signing in """
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['avatar', 'username', 'first_name', 'email']
