from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime
from .models import Question


class QuestionTests(TestCase):
    """
    Tests used for the Question model.
    """
    def test_is_recent_future(self):
        """
        Test for a question exactly over one day old.
        """
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(published_date=time)
        self.assertIs(future_question.is_recent(), False)

    def test_is_recent(self):
        """
        Test for a question exactly under one day old.
        """
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(published_date=time)
        self.assertIs(future_question.is_recent(), True)


def create_question(question_text, days):
    """
    Function used to create a question for the tests.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionIndexTests(TestCase):
    def test_null_questions(self):
        """
        Test for a question that doesn't exist.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        """
        Test for a question in the past.
        """
        question = create_question(question_text="Past", days=-7)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_future_question(self):
        """
        Test for a question in the future.
        """
        create_question(question_text="Future", days=7)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_future(self):
        """
        Test to only display past questions without future ones.
        """
        question = create_question(question_text="Past", days=-7)
        create_question(question_text="Future", days=7)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_double_past(self):
        """
        Test for multiple questions in the past.
        """
        question1 = create_question(question_text="Past 1", days=-7)
        question2 = create_question(question_text="Past 2", days=-14)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question2, question1])


class QuestionDetailTests(TestCase):
    def test_future_question(self):
        """
        Test for a question in the future.
        """
        future_question = create_question(question_text="Future.", days=7)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Test for a question in the past.
        """
        past_question = create_question(question_text="Past.", days=-7)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
