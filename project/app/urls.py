from django.contrib import admin
from django.urls import path, include
from .views import homepage, learn, push__or_eval_word, lesson_overview

urlpatterns = [
    path('', homepage),
    path("push_word/<action>/<index>", push__or_eval_word, name="push_word"),

    path("push_word", push__or_eval_word, name="push_word"),

    path("learn/<lection_id>", learn, name="learn"),

    path("overview", lesson_overview, name="overview"),
]
