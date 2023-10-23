""" Urls to navigate the stories app """
from . import views
from django.urls import path

urlpatterns = [
    path('', views.landingPage, name='landing_page'),
]
