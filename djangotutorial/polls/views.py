from django.db.models import F, Count, Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")[:5]


class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        return Question.objects.order_by("-published_date")


class CreateQuestionView(generic.CreateView):
    model = Question
    template_name = "polls/create_question.html"
    fields = ["question_text"]
    success_url = reverse_lazy("polls:index")


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"


class StatisticView(generic.ListView):
    template_name = "polls/statistics.html"
    context_object_name = "questions"
    model = Question

    def get_queryset(self):
        return Question.objects.annotate(total_choices=Count("choice"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_choices"] = self.get_queryset().aggregate(total=Count("choice"))["total"] or 0
        context["total_votes"] = Choice.objects.aggregate(total=Sum("votes"))["total"] or 0

        for question in context["questions"]:
            if question.choice_set.all().count() > 0:
                total_votes = question.choice_set.aggregate(total=Sum("votes"))["total"]
                average = total_votes / question.choice_set.all().count()
                question.average = 0 if average == 0 else round(average, 2)

        context["popular"] = max(Question.objects.all(), key=lambda q: q.get_total(), default=None)
        context["least_popular"] = min(Question.objects.all(), key=lambda q: q.get_total(), default=None)

        context["last_saved"] = Question.objects.get(id=Question.objects.aggregate(total=Max("id"))["total"])

        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      "polls/detail.html",
                      {
                          "question": question,
                          "error_message": "You didn't select a choice.",
                        },
                      )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
