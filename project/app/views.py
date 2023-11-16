from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
import random
import datetime
from .models import  Progress, Word, Sentence


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
        learn_modes = [build_sentence]  # multiple_choice , word_translation    place other learn methods as function here:
        random_choice = learn_modes[random.randint(0, len(learn_modes) - 1 )]
        return random_choice(request)
        
  
        
    elif request.method == "POST":
        learn_mode = cache.get('mode')
        match learn_mode:
            case "multiple_choice":
                word = Word.objects.filter(pk=int(cache.get("word")))[0]
                return eval_multiple_choice(request, word)
            case "word_translation":
                word = Word.objects.filter(pk=int(cache.get("word")))[0]

                return eval_word_translation(request, word)
            # and here for evaluation:
            case "sentence_building":
                sentence = Sentence.objects.filter(pk=int(cache.get("sentence")))[0]

                eval_sentence(request, sentence)
                    
        
def build_sentence(request): 
            if request.method == "GET":
    
                sentence = random.sample(list(Sentence.objects.all()), 1)[0]
                template = "app/build_sentence.html"
                words = sentence.get_words_en()
                context = {"sentence": sentence.sentence_de, "words":words}        
                
                cache.set('mode', 'sentence_building', 300)
                cache.set("sentence", sentence.id, 300)
                return render(request, template, context)
                
        
                
            elif request.method == "POST":
                    sentence = get_object_or_404(Sentence, pk=sentence_id)
                    selected_word = request.POST.get('selected_word')

                    # Fügen Sie das ausgewählte Wort zur Liste der bisher ausgewählten Wörter hinzu
                    constructed_sentence = request.session.get('constructed_sentence', [])
                    constructed_sentence.append(selected_word)
                    request.session['constructed_sentence'] = constructed_sentence

                    # Hier könnten Sie auch den Fortschritt des Benutzers speichern
                    # Zum Beispiel, wenn der Benutzer fertig ist, könnten Sie die Antwort überprüfen und Punkte vergeben

                    return JsonResponse({'constructed_sentence': constructed_sentence})
def eval_sentence(request, sentence):
    print("eval")            

def multiple_choice(request):
    """ Prepare a multiple choice question"""
    words = random.sample(list(Word.objects.all()), 4) # pick 4 cards
    
    cache.set('mode', 'multiple_choice', 300)
    cache.set("word", words[0].id)
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
    print(answer)
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


