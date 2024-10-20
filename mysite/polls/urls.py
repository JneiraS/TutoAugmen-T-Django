from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('all/', views.all_questions_by_pub_date, name='all'),
    path('<int:question_id>/frequency/', views.frequency, name='frequency'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('statistics/', views.statistics, name='statistics'),
    path('new_poll/', views.new_poll, name='new_poll'),
    path('chat-bot/', views.chat_bot, name='chat_bot'),
]
