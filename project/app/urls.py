from django.contrib import admin
from django.urls import path, include
from .views import homepage, learn, push__or_eval_word

urlpatterns = [
    path('', homepage),
    path("push_word/<action>/<index>", push__or_eval_word, name="push_word"),

    path("push_word", push__or_eval_word, name="push_word"),

    path("learn", learn, name="learn"),
]
