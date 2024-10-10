import datetime
from typing import Any

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.question_text} [Date de publication:{self.pub_date.date().strftime('%Y-%m-%d')}]"

    def was_published_recently(self):
        """Retourne True si la question a éé  publiée récemment."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age_question(self) -> int:
        """Retourne l'âge de la question en jours."""
        return (timezone.now() - self.pub_date).days

    def get_sum_votes(self):
        """Retourne la somme des votes de la question."""
        return sum(choice.votes for choice in self.choice_set.all())

    def get_choices(self) -> list[tuple[Any, Any, float | int | Any]]:
        """
        Retourne la liste des choix de la question ainsi que leur nombre de votes et leur proportions
        :return:
        """
        choices = self.choice_set.all()
        sum_votes = self.get_sum_votes() if self.get_sum_votes() > 0 else 1
        return [(choice.choice_text, choice.votes, choice.votes / sum_votes * 100) for choice in choices]

    def get_max_choice(self):
        """Retourne le choix avec le plus de votes."""
        choices = self.choice_set.all()
        return max(choices, key=lambda choice: choice.votes)

    @classmethod
    def most_or_least_popular_question(cls, order_by: str):
        """
        Retourne la question qui a le plus ou le moins de votes.
        :param order_by:  '-total_votes' ou  'total_votes'
        """
        # Ajoute un attribut total_votesà chaque question, qui correspond au nombre total de votes
        questions_with_total_votes = cls.objects.annotate(total_votes=models.Sum('choice__votes'))
        # Trie les questions par le nombre total de votes dans l'ordre décroissant
        ordered_questions = questions_with_total_votes.order_by(order_by)  #
        # retourne le premier element
        return ordered_questions.first()




class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
