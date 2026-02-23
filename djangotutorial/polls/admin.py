from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "published_date"]
    list_filter = ["question_text", "published_date"]
    ordering = ["published_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["question", "choice_text", "votes"]
    list_filter = ["question"]
    ordering = ["question", "votes"]
    search_fields = ["question", "choice_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
