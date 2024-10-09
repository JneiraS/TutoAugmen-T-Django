from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all_questions_by_pub_date, name='all'),
    path('<int:question_id>/frequency/', views.frequency, name='frequency'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('statistics/', views.statistics, name='statistics'),
]
