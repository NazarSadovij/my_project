from django.db import models
from django.contrib.auth.models import User
import random, string

# --- Розширення користувача ---
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Вчитель'),
        ('student', 'Учень'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# --- Клас ---
class Classroom(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classes')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, editable=False)
    students = models.ManyToManyField(User, related_name='joined_classes', blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.ascii_uppercase, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


# --- Вікторина ---
class Quiz(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='quizzes', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# --- Питання ---
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# --- Варіанти відповідей ---
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'вірно' if self.is_correct else 'ні'})"


# --- Результат ---
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.quiz.title} ({self.score}/{self.total})"
