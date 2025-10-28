from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Quiz, Question, Choice

# Форми для вікторини
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "question_type"]

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]

# Форма для реєстрації користувача
ROLE_CHOICES = (
    ('student', 'Учень'),
    ('teacher', 'Вчитель'),
)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Створюємо профіль користувача з роллю
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user
