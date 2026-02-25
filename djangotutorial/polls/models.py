import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField("published date")

    def __str__(self):
        return self.question_text[:20] + f" {self.published_date}"

    def is_recent(self):
        """
        Is the question's published date less than a day old.
        :return: True if it is less than a year old.
        """
        return self.published_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        """
        :return: The time elapsed between today and the published date.
        """
        time_elapsed = datetime.datetime.now(datetime.timezone.utc) - self.published_date
        return (f"{time_elapsed.days} days",
                f"{time_elapsed.seconds // 3600} minute(s)",
                f"{(time_elapsed.seconds // 60) % 60} second(s).")

    def get_choices(self):
        """
        Get the choices related to the question.
        :return: All the choices related.
        """
        resultat = self.choice_set.aggregate(total=models.Sum('votes'))
        total = resultat['total']
        if total == 0:
            return 0
        return [(c.choice_text, c.votes, c.votes * 100 / total)
                for c in self.choice_set.all()]

    def get_max_choices(self):
        """
        Get the highest amount of votes for a question.
        :return: The highest number of votes.
        """
        return Choice.objects.filter(question=self).aggregate(models.Max("votes"))


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text + f" {self.votes}"
