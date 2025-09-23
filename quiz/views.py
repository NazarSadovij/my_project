from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, Result
from .forms import QuizForm, QuestionForm, ChoiceForm

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz/home.html", {"quizzes": quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, "quiz/quiz_detail.html", {"quiz": quiz, "questions": questions})

def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect("quiz_detail", quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, "quiz/create_quiz.html", {"form": form})

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect("quiz_detail", quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, "quiz/add_question.html", {"form": form, "quiz": quiz})

def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect("quiz_detail", quiz_id=question.quiz.id)
    else:
        form = ChoiceForm()
    return render(request, "quiz/add_choice.html", {"form": form, "question": question})

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

        if request.user.is_authenticated:
            Result.objects.create(user=request.user, quiz=quiz, score=score, total=total)

        return render(request, "quiz/result.html", {"quiz": quiz, "score": score, "total": total})

    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "questions": questions})

def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = Result.objects.filter(quiz=quiz).order_by("-score", "created_at")
    return render(request, "quiz/leaderboard.html", {"quiz": quiz, "results": results})

@login_required
def user_results(request):
    results = Result.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "quiz/user_results.html", {"results": results})
