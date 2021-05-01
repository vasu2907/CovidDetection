from django.contrib import admin
from django.urls import path

from django.conf import *

from app.views import *

app_name = 'app'

urlpatterns = [
    path('', loginView),
    path('register', registerView),
    path('home', homeView),
    path('login', loginView),
    path('loginHandler', loginHandlerView),
    path('registerHandler', registerHandlerView),
    path('logout', logoutHandler),
    path('profile', profileView)
]