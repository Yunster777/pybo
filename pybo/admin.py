from django.contrib import admin
from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["subject"]
    list_display = ("id", "subject", "content")


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ["content"]
    list_display = ("id", "question", "content")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
