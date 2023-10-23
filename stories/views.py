from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def landingPage(request):
    """ Retrieves the landing page """
    return HttpResponse("Welcome to NarrAtive")
