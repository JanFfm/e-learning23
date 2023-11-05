from django.contrib import admin
from .models import Vocabulary, Progress, Word
# Register your models here.


admin.site.register(Word)    
admin.site.register(Vocabulary)    
admin.site.register(Progress)    