from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question, Choice, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]
