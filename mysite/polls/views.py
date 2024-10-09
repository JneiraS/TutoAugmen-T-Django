from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Question, Choice
from .forms import QuestionForm, QuestionChoiceForm


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


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


def new_poll(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect(reverse("polls:all"))

    else:
        form = QuestionForm()
    return render(request, "polls/new_poll.html", {"form": form})



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
