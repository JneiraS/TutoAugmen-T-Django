from django import forms

from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    choices = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="/!\    Entrez un choix par ligne."
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


# PARTIE OPTIONNELLE
class ChoiceForm(forms.ModelForm):
    """Formulaire de choix pour une question."""
    choice = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None,
        label='Choix'
    )

    class Meta:
        # Le modèle associé: Choice
        model = Choice
        fields = ['choice']

    def __init__(self, question_id, *args, **kwargs):
        """Initialise le formulaire avec les choix de la question."""
        super().__init__(*args, **kwargs)
        # Définition de la liste des choix pour le champ 'choice'
        self.fields['choice'].queryset = Choice.objects.filter(question_id=question_id)
