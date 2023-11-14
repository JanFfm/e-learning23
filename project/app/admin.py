from django.contrib import admin
from .models import  Progress, Word, Sentence
# Register your models here.


admin.site.register(Word)    
admin.site.register(Progress)    
admin.site.register(Sentence)