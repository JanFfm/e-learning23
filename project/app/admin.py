from django.contrib import admin
from .models import  Progress, Word, Sentence,LectionPorgress, Streak, ProgressPerHour
# Register your models here.


admin.site.register(Word)    
admin.site.register(Progress)    
admin.site.register(Sentence)
admin.site.register(LectionPorgress)
admin.site.register(Streak)
admin.site.register(ProgressPerHour)