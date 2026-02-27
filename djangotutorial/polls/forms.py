from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    choice_1 = forms.CharField(max_length=200, required=False, label='Choix 1')
    choice_2 = forms.CharField(max_length=200, required=False, label='Choix 2')
    choice_3 = forms.CharField(max_length=200, required=False, label='Choix 3')
    choice_4 = forms.CharField(max_length=200, required=False, label='Choix 4')
    choice_5 = forms.CharField(max_length=200, required=False, label='Choix 5')

    class Meta:
        model = Question
        fields = ['question_text']
        labels = {'question_text': 'Question'}
