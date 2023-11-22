from django.contrib import admin
from .models import  Progress, Word, Sentence,LectionProgress, Streak, ProgressPerHour
# Register your models here.


admin.site.register(Word)    
admin.site.register(Progress)    
admin.site.register(Sentence)
admin.site.register(LectionProgress)
admin.site.register(Streak)
admin.site.register(ProgressPerHour)