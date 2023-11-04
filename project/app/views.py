from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        if progress_obj.progress > 6:
            context, template = question.hard()
        elif progress_obj.progress > 3:
            context, template = question.middle()
        else:
            context, template = question.easy()
        return render(request, template, context)        
        
    elif request.method == "POST":
        question = Vocabulary.objects.get(pk=request.POST['pk'])
        progress_obj = Progress.objects.get(user=request.user, card=question)
        print(request.POST)
        #bei Lückentext:
        answer = ""
        if 'gap' in request.POST:
             answer = str(request.POST['gap'])
             print(answer)
        
       
        elif 'radio' in request.POST:
            answer = str(request.POST['radio'])
       
        elif 'reading' in request.POST:
            if str(request.POST['reading'])[0] == "1":
                messages.success(request, "Sehr gut!")
                progress_obj.increase()
                progress_obj.save()        
                return redirect("learn")
            else:
                messages.info(request, "Versuchs weiter!")
                progress_obj.decrease()
                progress_obj.save()        
                return redirect("learn")              
            
            
           
        if answer == question.right_translation:
                messages.success(request, "Das war richtig.")
                progress_obj.increase()
        else:
                messages.error(request, "Das war leider falsch!")
                progress_obj.decrease()
        progress_obj.save()
        
        return redirect("learn")