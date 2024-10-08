import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.question_text} [Date de publication:{self.pub_date.date().strftime('%Y-%m-%d')}]"

    def was_published_recently(self):
        """Retourne True si la question a éé  publiée récemment."""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def age_question(self) -> int:
        """Retourne l'âge de la question en jours."""
        return (timezone.now() - self.pub_date).days

    def get_choices(self) -> list[tuple[str, int]]:
        """Retourne la liste des choix de la question ainsi que leur nombre de votes."""
        choices = self.choice_set.all()
        return [(choice.choice_text, choice.votes) for choice in choices]

    def get_max_choice(self):
        """Retourne le choix avec le plus de votes."""
        choices = self.choice_set.all()
        return max(choices, key=lambda choice: choice.votes)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
