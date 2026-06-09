from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice, Result


# Home Page – List all quizzes
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})


# Enter Name Before Starting Quiz
def enter_name(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        request.session['user_name'] = request.POST.get('name', 'Guest')
        return redirect('quiz', quiz_id=quiz.id)

    return render(request, 'quiz/enter_name.html', {'quiz': quiz})


# Quiz Page
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                choice = Choice.objects.filter(
                    id=selected,
                    question=question
                ).first()

                if choice and choice.is_correct:
                    score += 1

        total = questions.count()

        # Save to session
        request.session['score'] = score
        request.session['total'] = total

        # Save result in database
        Result.objects.create(
            quiz=quiz,
            user_name=request.session.get('user_name', 'Guest'),
            score=score,
            total=total
        )

        return redirect('result', quiz_id=quiz.id)

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })


# Result Page
def result_view(request, quiz_id):
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    return render(request, 'quiz/result.html', {
        'score': score,
        'total': total,
        'quiz_id': quiz_id
    })


# Leaderboard
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = Result.objects.filter(quiz=quiz).order_by('-score')

    return render(request, 'quiz/leaderboard.html', {
        'quiz': quiz,
        'results': results
    })


# Admin Dashboard
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/admin/dashboard.html', {
        'quizzes': quizzes
    })


# Create Quiz
def create_quiz(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        quiz = Quiz.objects.create(
            title=title,
            description=description
        )

        return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'quiz/admin/create_quiz.html')


# Add Questions to Quiz
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        question_text = request.POST.get('question_text')
        options = request.POST.getlist('options[]')
        correct_option = int(request.POST.get('correct_option', 0))

        # Create Question
        question = Question.objects.create(
            quiz=quiz,
            question_text=question_text
        )

        # Create Choices
        for idx, option_text in enumerate(options):
            Choice.objects.create(
                question=question,
                option_text=option_text,
                is_correct=(idx == correct_option)
            )

        # Stay on same page to add more questions
        return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'quiz/admin/add_question.html', {
        'quiz': quiz
    })