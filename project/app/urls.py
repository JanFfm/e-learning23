from django.contrib import admin
from django.urls import path, include
from .views import homepage, learn

urlpatterns = [
    path('', homepage),
    path("learn", learn, name="learn")
]
