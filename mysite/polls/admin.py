from django.contrib import admin

from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'pub_date', 'was_published_recently', 'age_question')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    MAX_LENGTH = 20

    @admin.display(description='Question (tronquée)')
    def question_text_short(self, obj):
        """Tronque le texte de la question à 20 caractères"""
        return (obj.question_text[:QuestionAdmin.MAX_LENGTH] +
                ('...' if len(obj.question_text) > QuestionAdmin.MAX_LENGTH else ''))


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes')
    list_filter = ['votes', 'question']
    search_fields = ['choice_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
