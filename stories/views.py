from django.http import HttpResponse
from django.template import loader

# Create your views here.


def landingPage(request):
    """ Retrieves the landing page """
    land_page = loader.get_template('landing_page.html')
    return HttpResponse(land_page.render())
