from django.contrib import admin
from .models import  Progress, Word, Sentence,LectionProgress, Streaks, ProgressPerHour, TimeStamp,ProgressSentence
# Register your models here.


admin.site.register(Word)    
admin.site.register(Progress)  
admin.site.register(ProgressSentence)  
admin.site.register(Sentence)
admin.site.register(LectionProgress)
admin.site.register(Streaks)
admin.site.register(ProgressPerHour)
admin.site.register(TimeStamp)