import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField("published date")

    def __str__(self):
        return self.question_text[:20] + f" {self.published_date}"

    def is_recent(self):
        return self.published_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        time_elapsed = datetime.datetime.now(datetime.timezone.utc) - self.published_date
        return (f"{time_elapsed.days} days",
                f"{time_elapsed.seconds // 3600} minute(s)",
                f"{(time_elapsed.seconds // 60) % 60} second(s).")

    def get_choices(self):
        return Choice.objects.filter(question=self)

    def get_max_choices(self):
        return Choice.objects.filter(question=self).aggregate(models.Max("votes"))


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text + f" {self.votes}"
