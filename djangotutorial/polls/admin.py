from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "published_date"]
    list_filter = ["published_date"]
    ordering = ["published_date"]
    search_fields = ["question_text"]

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["published_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInLine]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["question", "choice_text", "votes"]
    list_filter = ["question"]
    ordering = ["question", "votes"]
    search_fields = ["question", "choice_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
