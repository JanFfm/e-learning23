from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
import random
import datetime
from .models import  Progress, Word


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
        learn_modes = [multiple_choice, word_translation]  # place other learn methods as function here:
        random_choice = learn_modes[random.randint(0, len(learn_modes) - 1 )]
        return random_choice(request)
        
  
        
    elif request.method == "POST":
        learn_mode = cache.get('mode')
        word = Word.objects.filter(pk=int(cache.get("word")))[0]
        match learn_mode:
            case "multiple_choice":
                return eval_multiple_choice(request, word)
            case "word_translation":
                return eval_word_translation(request, word)
            # and here for evaluation:
        
       
    
def multiple_choice(request):
    """ Prepare a multiple choice question"""
    words = Word.objects.all().order_by('?')[:4] # pick 4 cards
    
    cache.set('mode', 'multiple_choice', 30)
    cache.set("word", words[0].pk)
    question = words[0].word
    possible_answers = [w.translation for w in words]
    random.shuffle(possible_answers)
    print(possible_answers)
    template = "app/multiple_choice.html"
    return render(request, template,context={"question": question, 
                                             "possible_answers": possible_answers })
    
def eval_multiple_choice(request, word: Word):
    print(request.POST)
    progress_obj, _ = Progress.objects.get_or_create(user=request.user, word=word)

    answer = request.POST['answer']
    if answer.lower()  == word.translation.lower():
        messages.success(request, "Das war richtig.")
        progress_obj.increase()
    else:
        messages.error(request, "Das war leider falsch!")
        progress_obj.decrease()
    return redirect("learn")

        


def word_translation(request):
    word = Word.objects.all().order_by('?').first()
    cache.set('mode', 'word_translation', 30)
    cache.set("word", word.pk)
    
    question = word.word
    
    template = "app/translate_word.html"
    return render(request, template,context={"question": question} )

def eval_word_translation(request, word: Word):
    return eval_multiple_choice(request, word)


