from django.shortcuts import render
from  django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
# Create your views here.
import requests

from json import JSONEncoder
import json
import sys
import urllib

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def loginView(request):
    return render(request, 'login.html', {})

def registerView(request):
    return render(request, 'register.html', {})

def homeView(request):
    return render(request, 'home.html', {})

def loginHandlerView(request):
    print("Inside loginHandler View")
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username != None and password != None:
        request.session['username'] = username
        request.session['password'] = password
    else:
        username = request.session['username']
        password = request.session['password']
    test = Users.objects.filter(username = username).filter(password = password)
    print(test)
    if test:
        print("Valid User")
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect("/")

def registerHandlerView(request):
    print('Inside Register Handler')
    errors = []
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Username {username} and password {password}')
        if username is None or len(str(username).strip()) == 0:
            errors.append('Username is empty')
        if password is None or len(str(password).strip()) == 0:
            errors.append('Password is empty')
        print(errors)
        if len(errors) > 0:
            request.path_info = '/register'
            return HttpResponseRedirect(reverse('/register'), {})
        newUser = Users(username = username, password = password)
        newUser.save()
    except Exception as e:
        errors.append(e)
        return HttpResponseRedirect('/register', {})
    return render(request, 'login.html', {})
