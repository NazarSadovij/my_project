from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('class/<int:class_id>/results/', views.class_results, name='class_results'),
    path('class/<int:class_id>/create_quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
