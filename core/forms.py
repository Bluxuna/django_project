from django import forms
from core.models import Choise, Question
from users.models import User


class ChoiceVoteForm(forms.ModelForm):
    class Meta:
        model = Choise
        fields = '__all__'


class QuestionCreateForm(forms.ModelForm):
    def __init__(self, *args, user:User, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['question_text']

    def save(self, commit=True):
        question: Question = super().save(commit=False)
        question.user = self.user
        question.save()
        return question
    
    
