from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from .forms import SupportForm

class TermsView(TemplateView):
    """ Terms and Conditions of NarrAtive """
    template_name = "tos.html"

    def get_context_data(self, **kwargs):
        """ Retrieves data about the app to include in Terms """
        data = super(TermsView, self).get_context_data(**kwargs)
        data['company'] = settings.SITE_NAME
        data['country'] = settings.SITE_LOCATION
        return data


class PrivacyView(TemplateView):
    """ User data privacy policy at NarrArtive """
    template_name = "privacy-policy.html"

    def get_context_data(self, **kwargs):
        """ Retrieves data about the app to include in privacy policy """
        data = super(PrivacyView, self).get_context_data(**kwargs)
        data['company'] = settings.SITE_NAME
        return data


class SupportView(FormView):
    template_name = "support.html"
    form_class = SupportForm

    def get_success_url(self):
        return reverse("support") + "?success=True"

    def get_context_data(self, **kwargs):
        data = super(SupportView, self).get_context_data(**kwargs)
        data['success'] = bool(self.request.GET.get("success", False))
        return data

    def form_valid(self, form):
        send_mail(
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=[settings.SUPPORT_EMAIL]
        )
        return super(SupportView, self).form_valid(form)


class SiteMapView(TemplateView):
    template_name = "sitemap.xml"
    content_type = "application/xml"


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"
