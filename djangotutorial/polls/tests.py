from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime
from .models import Question


class QuestionTests(TestCase):
    def test_is_recent_future(self):
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(published_date=time)
        self.assertIs(future_question.is_recent(), False)

    def test_is_recent(self):
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(published_date=time)
        self.assertIs(future_question.is_recent(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionIndexTests(TestCase):
    def test_null_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        question = create_question(question_text="Past", days=-7)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_future_question(self):
        create_question(question_text="Future", days=7)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_future(self):
        question = create_question(question_text="Past", days=-7)
        create_question(question_text="Future", days=7)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_double_past(self):
        question1 = create_question(question_text="Past 1", days=-7)
        question2 = create_question(question_text="Past 2", days=-14)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question2, question1])
