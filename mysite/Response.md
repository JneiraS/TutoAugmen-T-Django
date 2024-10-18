# Questions:
- Dans le cours, vous avez déjà ajouté une interface de la classe __Question__. Faites de même avec la
  classe __Choice__. Visualisez l'apparition de la nouvelle interface dans l'admin. de Django.
```python
from .models import Question, Choice
  
admin.site.register(Question)
admin.site.register(Choice)
```

---

3. Visualisez le résultat de vos saisies dans l'interface d'admin.
	- Oui

- Voyez-vous tous les attributs de vos classes ?
	- Oui
- Pouvez-vous filtrer vos données suivants tous les attributs ?
	- Non
- Pouvez-vous trier vos données suivants tous les attributs ?
	- Non
- Pouvez-vous chercher un contenu parmi tous les champs ?
	- Non

---

5. Ajoutez un nouvel utilisateur via l'interface d'admin. Ne lui donnez pas le "Statut équipe" ni le "Statut
   super-utilisateur". Déconnectez-vous et essayer de vous reconnecter avec ce nouveau compte. Y
   parvenez-vous ?
	- Non, impossible

## 2.2.2.2 Questions
1. Lister tous les objets de type Question :
```python
from polls.models import Question

questions = Question.objects.all()
	  
for question in questions:
	print(question)

```

2. Ajoutez un filtre sur la date de publication – portant par ex. sur un de ses composants4 suivants : year,
   month, day – de vos questions et lister un sous-ensemble de vos questions suivant les dates que vous avez
   saisies à l'exercice précédent.

```python
from datetime import datetime

from django.utils import timezone
from polls.models import Question

today = timezone.now()
date_filter = datetime(2024, 10, 4)
questions = Question.objects.filter(pub_date__lte=date_filter)

for question in questions:
	print(question)

```

```python
from polls.models import Question

q_id1_1 = Question.objects.filter(id=2)
print(q_id1_1)

# <QuerySet [<Question: Quelle est la part du méthane d'origine humaine qui provient de la culture du riz ?>]>

```

4. Faites une boucle pour afficher les attributs de chaque question et leurs choix associés.

```python
from polls.models import Question, Choice

questions = Question.objects.all()

for question in questions:
	print("Question:", question.question_text)
	print("Date de publication:", question.pub_date)

	choices = Choice.objects.filter(question=question)
	for choice in choices:
		print("- Choix:", choice.choice_text)

print()
```

5. Affichez le nombre de choix enregistrés pour chaque question.

```python
from polls.models import Question, Choice

questions = Question.objects.all()

for question in questions:
	print("Question:", question.question_text)

choices = Choice.objects.filter(question=question)
print("Nombre de choix:", choices.count())

print()
```

7. Triez les questions par ordre antéchronologique.

```python
from polls.models import Question

questions = Question.objects.order_by('-pub_date')

for question in questions:
	print("Question:", question.question_text)
	print("Date de publication:", question.pub_date)

	print()
```

8. [optionnel] Cherchez toutes les questions dont un mot est présent dans le texte de ses choix, en utilisant
   la recherche contains. Essayer d'utiliser Recherches traversant les relations pour obtenir une solution la
   plus synthétique possible.

```python
from polls.models import Question

questions = Question.objects.filter(question_text__icontains="toxiques")

for question in questions:
	print("Question:", question.question_text)
	print("Date de publication:", question.pub_date)

	print()

# Question: Quelle quantité de métaux lourds, solvants, boues toxiques et autres déchets industriels est déversée dans les eaux du monde chaque jour ?
# Date de publication: 2024-10-04 11:00:00+00:00
```

9. Créez une question en utilisant le shell.

```python
from polls.models import Question

question = Question(question_text="En quelle année le métro de Londres a-t-il été ouvert ?",
					pub_date="2024-03-15")
question.save()
```

10. Ajoutez 3 choix à cette question en utilisant le shell.

```python
In[29]:
from polls.models import Question

last_question_id = Question.objects.latest('id').id

In[30]:
from polls.models import Question, Choice

question = Question.objects.get(id=last_question_id)

choice1 = Choice(question=question, choice_text="1876", votes=0)
choice1.save()

choice2 = Choice(question=question, choice_text="1863", votes=0)
choice2.save()

choice3 = Choice(question=question, choice_text="1869", votes=0)
choice3.save()
```
11. Listez les questions publiées récemment.

```python
from polls.models import Question

questions = Question.objects.all()

for question in questions:
	if question.was_published_recently():
		print(question)
        
# En quelle année le métro de Londres a-t-il été ouvert ?
```
---
## 2.2.3 Exercice d'écriture de méthodes du modèle
1. Sur le même modèle, ajoutez une méthode nommée age() qui calcule l'âge de la question.
```python
# models.py
def age_question(self):
	"""Retourne l'âge de la question en jours."""
	return (timezone.now() - self.pub_date).days
```
*ajout de  ``age_question`` pour afficher la colonne*
````python
# admin.py
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'pub_date', 'was_published_recently', 'age_question')
...
````

2. Vous avez remarqué dans l'exercice précédent que l'affichage d'un objet des classes [...]
````python
# admin.py
@admin.display(description='Question (tronquée)') # modifie l'en-tête.
def question_text_short(self, obj):
    """Tronque le texte de la question à 20 caractères"""
    return obj.question_text[:20] + ('...' if len(obj.question_text) > 20 else '')
````
3. Modifiez la classe Question pour ajouter l'affichage de la date de publication lors de l'affichage d'une de ces instances.

```python
# models.py
def __str__(self):
    return f"{self.question_text} [Date de publication:{self.pub_date.date().strftime('%Y-%m-%d')}]"
```

4. Ajoutez une méthode à la classe Question nommée get_choices() [...]

```python
# models.py
def get_choices(self) -> list[tuple[Any, Any, float | int | Any]]:
    """
    Retourne la liste des choix de la question ainsi que leur nombre de votes et leur proportions
    :return:
    """
    choices = self.choice_set.all()
    sum_votes = self.get_sum_votes() if self.get_sum_votes() > 0 else 1
    return [(choice.choice_text, choice.votes, choice.votes / sum_votes * 100) for choice in choices]
```
5. Ajoutez une méthode à la classe Question nommée get_max_choice() [...

```python
def get_max_choice(self):
    """Retourne le choix avec le plus de votes."""
    choices = self.choice_set.all()
    return max(choices, key=lambda choice: choice.votes)
```

## 3.2 Exercice sur les parties 3 et 4

1. dans le template index.html, ajouter l'affichage de la date de publication du sondage.

```python
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a> ({{ question.pub_date }})</li>
```

2. ajoutez une page http://127.0.0.1:8000/polls/all/ qui liste tous les sondages avec leur numéro id et leur titre portant un lien vers leur page de détail

```python
# all.html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li> <a href="{% url 'polls:detail' question.id %}">Id:{{ question.id }} - {{ question.question_text }} ({{ question.pub_date }})</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
```python
    # polls/urls.py
...
    path('all/', views.all, name='all'),
...
```

3. dans cette même page http://127.0.0.1:8000/polls/all/, modifier le lien porté par chaque question [...]

```python
# all.html
{{ question.question_text }}

<ul>
{% for choice, votes , pourcentage in question.get_choices %}
    {%if votes <= 1 %}
<li>{{ choice }} : {{ votes }} vote, soit : {{ pourcentage }}%</li>
   {% else %}
    <li>{{ choice }} : {{ votes }} votes, soit : {{ pourcentage }}%</li>
 {% endif %}
    {% endfor %}
</ul>
```

4. ajoutez une page de statistiques http://127.0.0.1:8000/polls/statistics/ affichant :
- le nombre total de sondage enregistrés
```python
    total_questions = Question.objects.count()
```
- le nombre total de choix possibles
```python
    total_choices = Choice.objects.count()
```
le nombre total de votes
```python
    total_votes = Choice.objects.aggregate(Sum("votes"))
```
la moyenne du nombre de votes par sondage
```python
    average_votes = total_votes["votes__sum"] / total_questions
```
la question la plus et la moins populaire
```python
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
```
la dernierée question enregistrée
```python
last_question_added = Question.objects.last()
```
5. ajouter un formulaire

```python
#polls/forms.py
from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
```
