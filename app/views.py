from django.shortcuts import render
from  django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
# Create your views here.
import requests

from json import JSONEncoder
import json

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def loginView(request):
    return render(request, 'login.html', {})

def registerView(request):
    return render(request, 'register.html', {})

def homeView(request):
    return render(request, 'home.html', {})

# Create your views here.
