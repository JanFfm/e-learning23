from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
import datetime
from .models import Vocabulary, Progress


@login_required
def homepage(request):
    if request.method =="GET":
        context = {
            "date": datetime.datetime.now(),
        }
        return render(request,"app/dashboard.html", context)
    
    

@login_required
def learn(request):
    if request.method == "GET":
        question = Vocabulary.objects.all().order_by("?").first() # pick random question
     
        progress_obj = Progress.objects.get_or_create(user=request.user, card=question)[0]
        if progress_obj.progress > 10:
            context, template = question.hard()
        elif progress_obj.progress > 5:
            context, template = question.middle()
        else:
            context, template = question.easy()
        return render(request, template, context)        
        
    elif request.method == "POST":
        return redirect("learn")