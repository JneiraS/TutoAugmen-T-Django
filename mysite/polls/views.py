from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
               :5
               ]


def all_questions_by_pub_date(request):
    latest_question_list = Question.objects.order_by("-pub_date")
    context = {"latest_question_list": latest_question_list}

    return render(request, "polls/all.html", context)


def frequency(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    somme_votes = sum(choice.votes for choice in question.choice_set.all())
    context = {"question": question, "somme_votes": somme_votes}

    return render(request, "polls/frequency.html", context)


def statistics(request):
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(Sum("votes"))
    average_votes = total_votes["votes__sum"] / total_questions
    most_popular_questions = Question.most_or_least_popular_question('-total_votes')
    least_popular_questions = Question.most_or_least_popular_question('total_votes')
    last_question_added = Question.objects.last()

    context = {'nb_questions': total_questions, 'nb_choices': total_choices, 'nb_votes': total_votes,
               'average_votes': average_votes, 'mp_questions': most_popular_questions,
               'lp_questions': least_popular_questions, 'last_question': last_question_added}

    return render(request, "polls/statistics.html", context)


@login_required(login_url="/login/")
def new_poll(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("polls:all"))

    else:
        form = QuestionForm()
    return render(request, "polls/new_poll.html", {"form": form})


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    # PARTIE OPTIONNELLE
    def post(self, request, *args, **kwargs):
        # Créer une instance de ChoiceForm avec l'ID de la question et les données POST
        form = ChoiceForm(question_id=self.kwargs['pk'], data=request.POST)

        if form.is_valid():
            # On obtient la réponse choisie
            selected_choice = form.cleaned_data['choice']
            selected_choice.votes += 1
            selected_choice.save()
            return redirect(reverse("polls:index"))
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChoiceForm(question_id=self.kwargs['pk'])
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
