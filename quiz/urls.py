from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/create/", views.create_quiz, name="create_quiz"),
    path("quiz/<int:quiz_id>/add-question/", views.add_question, name="add_question"),
    path("question/<int:question_id>/add-choice/", views.add_choice, name="add_choice"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/leaderboard/", views.leaderboard, name="leaderboard"),
    path("my-results/", views.user_results, name="user_results"),
]
