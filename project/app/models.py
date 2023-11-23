from django.db import models
from django.contrib.auth import get_user_model # Create your models here.
from django.conf import settings
import random
import re
import string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import JSONField
from datetime import datetime, timedelta

class Word(models.Model):
    word = models.CharField(max_length=300)
    translation = models.CharField(max_length=300)
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
    
    def __str__(self):
        return self.word +": "+self.translation
         

class Sentence(models.Model):
    sentence_en = models.CharField(max_length=500)
    sentence_de = models.CharField(max_length=500)
    
    def get_words_en(self):
        words = re.sub(r'[^\w\s]', '', self.sentence_en).split(" ")
        random.shuffle(words)
        return words  
    def return_solution(self,selection:list):
        words = re.sub(r'[^\w\s]', '', self.sentence_en).split(" ")
        print(words, selection)
        if words == selection:
            return True
        return False
           
    
    def __str__(self):
         return self.sentence_en


'''
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

'''
#ToDO: Rangliste für User per h
# Gewichtete Fragen-Auswahl nach besten/schlechtesten
# Steak
# Statistik für Aufgabentypen
# statistiken nach versch. Zeitfenstern filtern
class TimeStamp(models.Model):
    date =models.DateField()
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    related_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    class Meta:
        unique_together = ('date', 'hour')
    
    def calculate_time_difference(self, other):
        my_time = datetime.combine(self.date, datetime.min.time()) + timedelta(hours=self.hour)
        other_time = datetime.combine(other.date, datetime.min.time()) + timedelta(hours=other.hour)
        time_difference = abs(my_time - other_time)
        return time_difference.total_seconds() / 3600
    def __str__(self):
        return f"{self.date}: {self.hour}:00"


class Streaks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    learning_times = models.ManyToManyField(TimeStamp)    
    
    def print_times(self):
        return str(self.learning_times.all())
    def add_time(self, time):
        print(self.learning_times)
        if time not in self.learning_times:
            self.learning_times.add(time)
            self.save()
            self.check_streak()
            
            
    def count_streaks(self):
        print(self.learning_times.all())

        sorted_learning_times = sorted(self.learning_times.all(), key=lambda x: (x.date, x.hour))
        longest_streak = 0
        act_streak = 1

        for i, timestamp in enumerate(sorted_learning_times[1:], start=1):
            time_difference = timestamp.calculate_time_difference(sorted_learning_times[i - 1])
            if time_difference <= 1:
                act_streak += 1
            else:
                longest_streak = max(longest_streak, act_streak)
                act_streak = 1
        if longest_streak == 0:
            longest_streak = act_streak
     
        return longest_streak, act_streak
    
    def check_if_in_streak(self, time_stamp): 
        print(__name__)  
      
        if (len(self.learning_times.all())) == 0:
            print("len")
            return False
        sorted_learning_times = sorted(self.learning_times.all(), key=lambda x: (x.date, x.hour))

        time_difference = time_stamp.calculate_time_difference(sorted_learning_times[-1])
        print(time_difference)
        if time_difference > 1:
            return False
        else:
            return True

        
            
        



    


class ProgressPerHour(models.Model):
    time_stamp = models.ForeignKey(TimeStamp, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    word_count = models.IntegerField()
    correct_word_count = models.IntegerField()
    
    sentence_count = models.IntegerField()
    correct_sentence_count = models.IntegerField()
    class Meta:
        unique_together = ('user', 'time_stamp')


    

class LectionProgress(models.Model):
    lection_number = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    progress = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    def get_progress(self):
        return self.progress
    def __str__(self):
        return "Vortschritt in Lektion {0} für {1}".format(self.lection_number, self.user)


class Progress(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    progress = models.IntegerField(default=0)
    
    class Meta:
            unique_together = (('word', 'user'),)
    def __str__(self):
         return str(self.word) +", "+ str(self.user) + " Progress: " + str(self.progress)

    
    def decrease(self):
        if self.progress > 0:
            self.progress -= 1
            self.save()
            
    def increase(self):
          if self.progress < 9:
                self.progress += 1
                self.save()


class ProgressSentence(Progress):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
    word = None

    