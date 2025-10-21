from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Аутентифікація
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Панелі користувачів
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard"),

    # Вікторини
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),

    # Результати
    path("class/<int:class_id>/results/", views.class_results, name="class_results"),
]
