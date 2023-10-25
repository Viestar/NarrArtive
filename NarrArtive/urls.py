"""
URL configuration for NarrArtive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from stories.views import *
from .views import (
    HomeView,
    TermsView,
    PrivacyView,
    SupportView,
    SiteMapView,
    RobotsView
)

urlpatterns = [
    path(
        # Cleared
        route='',
        view=HomeView.as_view(),
        name="home"
    ),
    path(
        # Cleared
        route='terms-of-service/',
        view=TermsView.as_view(),
        name="tos"
    ),
    path(
        route='privacy-policy/',
        view=PrivacyView.as_view(),
        name="privacy"
    ),
    path(
        route='support/',
        view=SupportView.as_view(),
        name="support"
    ),
    path(
        route='sitemap.xml',
        view=SiteMapView.as_view(),
        name="sitemap"
    ),
    path(
        route='robots.txt',
        view=RobotsView.as_view(),
        name="robots"
    ),
    # path(
    #     route='stripe/',
    #     view=include(
    #         "djstripe.urls",
    #         namespace="djstripe"
    #     ),
    # ),
    path(
        route='auth/',
        view=include('allauth.urls')
    ),
    path(
        route='admin/',
        view=admin.site.urls,
    ),
    # path(
    #     route='captcha/',
    # ),
]
