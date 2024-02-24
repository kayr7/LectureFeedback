from django import forms
from .models import Question, Choice

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            if question.question_type == 'MC':
                # Ensure you use the correct related name here
                choices = question.choices.all()  # This should match your related_name
                self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                    queryset=choices,
                    widget=forms.RadioSelect,
                    label=question.question_text,
                    required=True,
                )
            elif question.question_type == 'FT':
                self.fields[f'question_{question.id}'] = forms.CharField(
                    widget=forms.Textarea,
                    label=question.question_text,
                    required=True,
                )
