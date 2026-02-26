from django.test import TestCase
from django.utils import timezone

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
