from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(QuizTaker)
admin.site.register(QuizMaker)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizInstance)
admin.site.register(QuestionInstance)
