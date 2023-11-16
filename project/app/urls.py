from django.contrib import admin
from django.urls import path, include
from .views import homepage, learn#, push_word

urlpatterns = [
    path('', homepage),
    path("learn", learn, name="learn"),
    #path("learn/push_word", push_word, name="push_word")
]
