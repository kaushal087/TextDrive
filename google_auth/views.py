from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('google_auth/home.html')
    context = {}
    return HttpResponse(template.render(context, request))
