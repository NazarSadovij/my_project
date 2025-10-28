from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question, Choice, Result, Classroom, UserProfile
from django.contrib.auth.models import User
from .forms import QuizForm, QuestionForm, ChoiceForm
from django.forms import inlineformset_factory

# --- Головна сторінка ---
@login_required
def home(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

# --- Панель вчителя ---
@login_required
def teacher_dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role != 'teacher':
        messages.error(request, "Доступ заборонено.")
        return redirect('home')

    classes = Classroom.objects.filter(teacher=request.user)

    # Створення нового класу
    if request.method == "POST":
        name = request.POST.get("class_name")
        if name:
            Classroom.objects.create(teacher=request.user, name=name)
            messages.success(request, f"Клас '{name}' створено успішно!")

    return render(request, "quiz/teacher_dashboard.html", {"classes": classes})

# --- Панель учня ---
@login_required
def student_dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role != 'student':
        messages.error(request, "Доступ заборонено.")
        return redirect('home')

    # Приєднання до класу по коду
    if request.method == "POST":
        code = request.POST.get("class_code").upper()
        classroom = Classroom.objects.filter(code=code).first()
        if classroom:
            classroom.students.add(request.user)
            messages.success(request, f"Ви приєдналися до класу {classroom.name}")
        else:
            messages.error(request, "Клас із таким кодом не знайдено")

    classes = request.user.joined_classes.all()
    return render(request, "quiz/student_dashboard.html", {"classes": classes})

# --- Створення вікторини ---
@login_required
def create_quiz(request, class_id):
    classroom = get_object_or_404(Classroom, id=class_id, teacher=request.user)
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.created_by = request.user
            quiz.classroom = classroom
            quiz.save()
            messages.success(request, "Вікторина створена!")
            return redirect('teacher_dashboard')
    else:
        quiz_form = QuizForm()
    return render(request, "quiz/create_quiz.html", {"quiz_form": quiz_form, "classroom": classroom})

# --- Перегляд вікторини ---
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "quiz/quiz_detail.html", {"quiz": quiz})

# --- Проходження вікторини ---
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                choice = question.choices.filter(id=selected, is_correct=True).first()
                if choice:
                    score += 1

        classroom = quiz.classroom
        Result.objects.create(
            user=request.user,
            quiz=quiz,
            classroom=classroom,
            score=score,
            total=total,
        )

        return render(
            request,
            "quiz/result.html",
            {"quiz": quiz, "score": score, "total": total},
        )

    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "questions": questions})

# --- Перегляд результатів учителем ---
@login_required
def class_results(request, class_id):
    classroom = get_object_or_404(Classroom, id=class_id, teacher=request.user)
    results = Result.objects.filter(classroom=classroom).select_related("user", "quiz")
    return render(request, "quiz/class_results.html", {"classroom": classroom, "results": results})
