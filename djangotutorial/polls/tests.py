from django.test import TestCase
from django.utils import timezone

import datetime
from .models import Question


class QuestionTests(TestCase):
    def test_is_recent(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(published_date=time)
        self.assertIs(future_question.is_recent(), False)
