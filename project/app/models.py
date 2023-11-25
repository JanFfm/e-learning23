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
    lection = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.word +": "+self.translation + " (Lektion: " + str(self.lection) +")"
    class Meta:
        ordering = ("lection", "word")
         

class Sentence(models.Model):
    sentence_en = models.CharField(max_length=500)
    sentence_de = models.CharField(max_length=500)
    lection = models.PositiveIntegerField(default=1)
    
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
    count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    

    class Meta:
        unique_together = ('user', 'time_stamp')
        ordering = ('user', 'time_stamp')


    

class LectionProgress(models.Model):
    lection_number = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    progress = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0)

    unlocked = models.BooleanField(default=False)
    tmp_lection_prg = models.PositiveIntegerField(default=0)
    def calc_progress(self, user):
        words_in_lection = Word.objects.filter(lection=self.lection_number)
        sentences_in_lection =Sentence.objects.filter(lection=self.lection_number)
        hundret_percent = (len(words_in_lection)+ len(sentences_in_lection)) * 10 + 0.000001
        progress_count = 0
        for w in words_in_lection:
            p = Progress.objects.get(word=w, user=user)            
            progress_count += p.progress
        for s in sentences_in_lection:
            p = ProgressSentence.objects.get(sentence=s, user=user)            
            progress_count += p.progress
            print(progress_count , hundret_percent, progress_count / hundret_percent)
        self.progress = progress_count / hundret_percent
        self.save()


    def unlock(self):
        self.unlocked = True
        self.save()

    def increase_tmp_prg(self):
        self.tmp_lection_prg = self.tmp_lection_prg + 1
        self.save()

    def reset_tmp_prg(self):
        self.tmp_lection_prg = 0
        self.save()

    def get_tmp_prg(self):
        return self.tmp_lection_prg
    
    
    def get_progress(self):
        return self.progress
    def __str__(self):
        return "Fortschritt in Lektion {0} für {1}".format(self.lection_number, self.user)


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
          if self.progress < 11:
                self.progress += 1
                self.save()


class ProgressSentence(Progress):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
    word = None

    