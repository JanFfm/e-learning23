from django.db import models
from django.contrib.auth import get_user_model # Create your models here.
from django.conf import settings
import random

class Word(models.Model):
    word = models.CharField()
    translation = models.CharField()
    WORD_CHOICES = (
        ("1", "noun"),  
        ("2", "verb"),
        ("3","adverb"),
        ("4","adjective"),
        ("5","pronoun"),
        ("6","preposition"),
        ("7","conjunction"),
        ("8","interjection"),
        ("9","determiner"))
    part_of_speech = models.CharField(choices=WORD_CHOICES, max_length=1)
         
    



class Vocabulary(models.Model):
    original_word = models.CharField(max_length=200)

    right_translation = models.CharField(max_length=200)
    wrong_aswers = models.JSONField() # for multiple choice
    gap_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.original_word+ ": " + self.right_translation
    def easy(self):
        """Einprägen
        """
        context = {
            "pk": self.pk,
            "original_word": self.original_word, 
            "right_translation": self.right_translation
        }
        template = "app/reading.html"
        return context, template
    def middle(self):
        """Multiple Choice
        l : list of possible answers
        """
        l =self.wrong_aswers['0']
        l.append(self.right_translation)
        random.shuffle(l)
        context = {
            "pk": self.pk,
            "data":l, 
            "original_word": self.original_word}
        template = "app/multiple_choice.html"
        return context, template


    def hard(self):
        """Lückentext
        """
        context = {"pk": self.pk,
                   "gap_text": self.gap_text}
        template = "app/gap_text.html"
        return context, template





class Progress(models.Model):
    card = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    progress = models.IntegerField(default=0)
    
    def decrease(self):
        if self.progress > 0:
            self.progress -= 1
            
    def increase(self):
          if self.progress < 9:
                self.progress += 1
