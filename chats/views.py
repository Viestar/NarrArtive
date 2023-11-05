from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def chat_view(request, recipient_username):
    """ Returns whole chat"""
    return render(request, 'chat.html', {'recipient_username': recipient_username})
