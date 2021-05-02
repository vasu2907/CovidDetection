from django.shortcuts import render
from  django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
from .utils import *
import requests
import joblib
from json import JSONEncoder
import json
import sys, os
import urllib
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import *
from keras.models import * 
from keras.preprocessing import image

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def loginView(request):
    username = request.session.get('username', None)
    password = request.session.get('password', None)
    if username != None and password != None:
        return HttpResponseRedirect('/home')
    return render(request, 'login.html', {})

def registerView(request):
    username = request.session.get('username', None)
    password = request.session.get('password', None)
    if username != None and password != None:
        return HttpResponseRedirect('/home')
    return render(request, 'register.html', {})

def homeView(request):
    username = request.session.get('username', None)
    password = request.session.get('password', None)
    if username == None or password == None:
        return HttpResponseRedirect('/')
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

def logoutHandler(request):
    request.session['username'] = None
    request.session['password'] = None
    request.session.flush()
    return HttpResponseRedirect('/')

def profileView(request):
    username = request.session.get('username', None)
    password = request.session.get('password', None)
    if username == None or password == None:
        return HttpResponseRedirect('/')
    user = Users.objects.filter(username = username).filter(password = password)
    return render(request, 'profile.html', {'user': user[0]})

def dataHandler(request):
    y_actual, y_test = [],[]
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phoneNumber = request.POST.get('phoneNumber', '').strip()
    try:
        imageFile = request.FILES.get('sampleImage').read()
        testFile = open('tmp/sampleTest.png', 'wb')
        testFile.write(imageFile)
        testFile.close()
    except:
        return HttpResponseRedirect('/home')
    if name == '' or email == '' or phoneNumber == '':
        return HttpResponseRedirect('/home')

    ROOT_DIR =  os.path.dirname(os.path.abspath(__file__))
    modelPath = ROOT_DIR + '/../model_covid.h5'
    model=load_model('/home/vasu/projects/CovidDetection/model_covid.h5')
    img=image.load_img('tmp/sampleTest.png',target_size=(224,224))
    img=image.img_to_array(img)
    img=np.expand_dims(img,axis=0)
    pred=model.predict(img)
    # print(pred)
    y_test.append(pred[0,0])
    
    print(f'y_test is {y_test}')
    covidResult = ''
    if int(y_test[0]) == 0:
        covidResult = 'Positive'
    else:
        covidResult = 'Negative'

    mailSuccess = send_covid_email(name, email, covidResult)
    print(mailSuccess)
    return render(request, 'home.html', {'result': covidResult})
