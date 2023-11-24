from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect
import random
from datetime import datetime
from .models import  Progress, Word, Sentence, ProgressSentence, Streak, LectionProgress
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr
import pyttsx3


@login_required
def homepage(request):
    if request.method =="GET":
        context = {
            "date": datetime.now(),
        }
        return render(request,"app/dashboard.html", context)
    

@login_required
def lesson_overview(request):
    if request.method == "GET":
        
        lection_progress = LectionProgress.objects.all().filter(user=request.user).order_by('id')
        
        for i in range(len(lection_progress)):
            if lection_progress[i].get_progress() > 0.95:
                if i+1 <= len(lection_progress):
                    lection_progress[i+1].unlock()
            
    
       # print(lection_progress.get(user=request.user, lection_number=1).get_progress())
        context = {
            "lection_progress": lection_progress,
                   }
        return render(request, "app/overview.html", context)


@login_required
def learn(request, lection_id):

    #TODO maybe a total of 15 question and the return to main menu?
    curr_lection_prg = LectionProgress.objects.filter(user=request.user, lection_number=lection_id).first()
    if(not curr_lection_prg.unlocked):
        messages.error(request, "Diese Übung ist noch nicht freigeschaltet!")
        return redirect(lesson_overview)
    
    if(curr_lection_prg.get_tmp_prg() == 10): #number of questions can be adjusted here. 10 -> leads to 5 questions
        curr_lection_prg.reset_tmp_prg()
        messages.success(request, "Übung {0} erfolgreich beendet!".format(lection_id))
        return redirect(lesson_overview)
    else:
        curr_lection_prg.increase_tmp_prg()


    if request.method == "GET":
        
        streak, _ = Streak.objects.get_or_create(user=request.user)
        streak.add_time(str(datetime.now().today().date())+","+str(datetime.now().hour)+":00")
        
        learn_modes = [multiple_choice, word_translation, listening_comprehension, speaking_exercice, build_sentence]  # place other learn methods as function here:
        random_choice = learn_modes[random.randint(0, len(learn_modes) - 1 )]
        return random_choice(request, lection_id)
   
        
    elif request.method == "POST":
        learn_mode = cache.get('mode')
        word = cache.get("word", None)
        try:
            word = Word.objects.filter(pk=int(word))[0]
        except:
            word = None 
        
        match learn_mode:
            case "multiple_choice":
                return eval_multiple_choice(request, word, lection_id)
            case "word_translation":
                return eval_word_translation(request, word, lection_id)
            case "listening_comprehension":
                return eval_listening_comprehension(request, word, lection_id)
            case "speaking_exercice":
                return eval_speaking_exercice(request, word, lection_id)
            # and here for evaluation:
     

        
def build_sentence(request, lection_id): 
            if request.method == "GET":    
                sentence = random.sample(list(Sentence.objects.filter(lection=lection_id)), 1)[0]
                print(sentence.lection)
                template = "app/build_sentence.html"
                words = sentence.get_words_en()
                context = {"sentence": sentence.sentence_de, "words":words, "htmx_url": 'push_word', "pk": sentence.id, "target_id": "#word-container"}        
       
                return render(request, template, context)
                
        
       


@login_required
def push__or_eval_word(request, action=None, index=None):
    print(request.POST)
    if request.htmx: 
        if action and index: 
            index = int(index)
            words = request.POST.getlist('words')  if 'words' in request.POST.keys() else []
            selected_words = request.POST.getlist('selected_words') if 'selected_words' in request.POST.keys() else []


            if action=="push":
                selected_words.append(words[index])
                words.pop(index)
                
                context = {"words":words, "selected_words":selected_words, "htmx_url": 'push_word', "target_id": "#word-container"}        
                return render(request, "app/partials/sentence_building_partial.html", context)
            elif action=="pull":
                words.append(selected_words[index])
                selected_words.pop(index)
                context = {"words":words, "selected_words":selected_words, "htmx_url": 'push_word', "target_id": "#word-container"}      
                return render(request, "app/partials/sentence_building_partial.html", context)

                
            elif action == "check":
                if len(words) > 0:
                    context = {"words":words, "selected_words":selected_words, "htmx_url": 'push_word', "target_id": "#word-container", "message": "Bitte setze den Satz aus allen Wörtern zusammen!"}      
                    return render(request, "app/partials/sentence_building_partial.html", context)
                else:
                    print(selected_words)
                    sentence = Sentence.objects.get(pk=int(request.POST['pk']))
                    solution = sentence.return_solution(selected_words)
                    lection_id = sentence.lection
                    print("Value for lection id:", lection_id)
                    progress_obj, _ = ProgressSentence.objects.get_or_create(user=request.user, sentence=sentence)
                    
                    if solution:
                        progress_obj.increase()
                        messages.success(request, "Das war richtig.")

                    else:
                        progress_obj.decrease()
                        messages.error(request, "Das war leider falsch!")
                    return HttpResponseClientRedirect(str(lection_id)) # changed this from "learn" to str(lection_id) to get back to sub-url containing lesson index
                    #return redirect("learn", lection_id)

                                    

def multiple_choice(request, lection_id):
    """ Prepare a multiple choice question"""
    words = random.sample(list(Word.objects.filter(lection=lection_id)), 4) # pick 4 cards
    
    cache.set('mode', 'multiple_choice', 300)
    cache.set("word", words[0].id)
    question = words[0].word
    possible_answers = [w.translation for w in words]
    random.shuffle(possible_answers)
    print(possible_answers)
    template = "app/multiple_choice.html"
    return render(request, template,context={"question": question, 
                                             "possible_answers": possible_answers })
    
def eval_multiple_choice(request, word: Word, lection_id):
    print(request.POST)
    progress_obj, _ = Progress.objects.get_or_create(user=request.user, word=word)

    answer = request.POST['answer']
    print(answer)
    if answer.lower()  == word.translation.lower():
        messages.success(request, "Das war richtig.")
        progress_obj.increase()
    else:
        messages.error(request, "Das war leider falsch!")
        progress_obj.decrease()
    return redirect("learn", lection_id)

        


def word_translation(request, lection_id):
    word = Word.objects.filter(lection=lection_id).order_by('?').first()
    cache.set('mode', 'word_translation', 30)
    cache.set("word", word.pk)
    
    question = word.word
    
    template = "app/translate_word.html"
    return render(request, template,context={"question": question} )

def eval_word_translation(request, word: Word, lection_id):
    return eval_multiple_choice(request, word, lection_id)




def listening_comprehension(request, lection_id):

    word = Word.objects.filter(lection=lection_id).order_by('?').first()
    cache.set('mode', 'listening_comprehension', 30)
    cache.set("word", word.pk)

    question = word.word
    print("Word:", word.word, "Translation:", word.translation)
    tts = gTTS(question)
    print("saving file..")
    
    #mp3_fp = BytesIO()
    #tts.write_to_fp(mp3_fp)
    tts.save('media/hello.mp3')

    template = "app/listening_comprehension.html"
    return render(request, template, context={"question": question})

def eval_listening_comprehension(request, word: Word, lection_id):
    print(request.POST)
    progress_obj, _ = Progress.objects.get_or_create(user=request.user, word=word)

    answer = request.POST['answer']
    if answer.lower()  == word.translation.lower():
        messages.success(request, "Das war richtig.")
        progress_obj.increase()
    else:
        messages.error(request, "Das war leider falsch!")
        progress_obj.decrease()
    return redirect("learn", lection_id)


def speaking_exercice(request, lection_id):
    word = Word.objects.filter(lection=lection_id).order_by('?').first()
    cache.set('mode', 'speaking_exercice', 30)
    cache.set("word", word.pk)
    
    #question = word.word
    question = word.translation
    
    template = "app/speaking_exercice.html"
    return render(request, template,context={"question": question} )

def eval_speaking_exercice(request, word: Word, lection_id):
    print(request.POST)
    progress_obj, _ = Progress.objects.get_or_create(user=request.user, word=word)

    answer = request.POST['ans']
    print("This was the answer", answer)
    if answer.lower()  == word.word.lower():
        messages.success(request, "Das war richtig.")
        progress_obj.increase()
    else:
        messages.error(request, "Das war leider falsch!")
        progress_obj.decrease()
    return redirect("learn", lection_id)