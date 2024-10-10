from django import forms

from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    choices = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="Entrez un choix par ligne."
    )

    class Meta:
        model = Question
        fields = ['question_text', 'choices', 'pub_date']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def save(self, commit=True):
        """Sauvegarde les questions et les choix."""
        question = super().save(commit=False)
        if commit:
            question.save()
            choices = self.cleaned_data['choices'].split('\n')
            # Crée une instance de Choice pour chaque choix
            for choice_text in choices:
                # Crée une nouvelle instance de Choice avec la question et le texte de choix,
                Choice.objects.create(question=question, choice_text=choice_text.strip())
        return question


