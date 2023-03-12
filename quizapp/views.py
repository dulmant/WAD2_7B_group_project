from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from .decorators import *
from .models import Quiz, Question


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('quizapp:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'quizapp/index.html', {'username': request.user.username})


def register(request):
    registered = False

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.set_password(user.password)
            user.save()

            if user.user_type == 1:
                profile = QuizTaker.objects.create(user=user)
            else:
                profile = QuizMaker.objects.create(user=user)
            print(form['user_type'].value)

            profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            registered = True
            return redirect(reverse('quizapp:index'))
        else:
            print(form.errors)
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:

        form = UserForm()

    return render(request,
                  'quizapp/register.html',
                  context={'form': form,
                           'registered': registered})


def user_logout(request):
    logout(request)
    return redirect(reverse('quizapp:index'))


@quiz_taker_required
def quiz(request, quiz_slug):
    quiz_instance = get_object_or_404(Quiz, name_slug=quiz_slug)
    questions = Question.objects.filter(quiz=quiz_instance)
    question_data_list = []

    for question in questions:
        question_options = [question.correct_answer, question.incorrect_answer_1, question.incorrect_answer_2,
                   question.incorrect_answer_3]
        question_data = {'question': question, 'options': question_options}
        question_data_list.append(question_data)

    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_answer:
                actual_score = question.max_score
            else:
                actual_score = 0
            quiz_attempt = QuizAttempt.objects.update_or_create(
            quiz=quiz_instance,
            quiz_maker=quiz_instance.author,
            max_score=quiz_instance.max_score,
            actual_score=actual_score,
            quiz_taker=request.user
            )[0]
            answer = Answer.objects.create(
                quiz=quiz_instance,
                question=question,
                answer_choice=selected_option,
                max_score=question.max_score,
                actual_score=actual_score,
                quiz_attempt=quiz_attempt,
                quiz_taker=request.user,
            )

    context = {
        'quiz': quiz_instance,
        'questions': questions,
        'number_of_questions': quiz_instance.number_of_questions,
        'quiz_instance': quiz_instance,
        'question_data_list': question_data_list
    }
    return render(request, 'quizapp/quiz.html', context)



def about(request):
    return render(request, 'quizapp/about.html')


def contact(request):
    return render(request, 'quizapp/contact.html')


@quiz_maker_required
def quiz_maker_dashboard(request):
    has_quizzes = False
    if Quiz.objects.filter(author=request.user).exists():
        has_quizzes = True
    my_quizzes = Quiz.objects.filter(author=request.user)

    context = {'my_quizzes': my_quizzes, 'has_quizzes': has_quizzes}
    return render(request, 'quizapp/quizmaker.html', context)


@quiz_taker_required
def quiz_taker_dashboard(request):
    quizzes_exist = False
    if Quiz.objects.all().exists():
        quizzes_exist = True
    all_quizzes = Quiz.objects.all()

    context = {'all_quizzes': all_quizzes, 'quizzes_exist': quizzes_exist}
    return render(request, 'quizapp/quiztaker.html', context)


@quiz_maker_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            request.session['quiz_form_data'] = form.cleaned_data
            return redirect(reverse('quizapp:add_questions', kwargs={'quiz_slug': slugify(form.cleaned_data['name']),
                                                                     'number_of_questions': form.cleaned_data['number_of_questions']}))
    else:
        form = QuizForm()

    context = {"form": form, "username": request.user.username}
    return render(request, 'quizapp/create_quiz.html', context)


@quiz_maker_required
def add_questions(request, quiz_slug, number_of_questions):
    my_form_set = formset_factory(QuestionForm, extra=number_of_questions)

    quiz_form_data = request.session.get('quiz_form_data')
    if not quiz_form_data:
        # Redirect to create_quiz view if quiz_form_data not found in session
        return redirect(reverse('quizapp:create_quiz'))

    if request.method == 'POST':
        formset = my_form_set(request.POST)
        if formset.is_valid():
            overall_max_score = 0
            quiz = Quiz.objects.create(name=quiz_form_data['name'],
                                        topic=quiz_form_data['topic'],
                                        number_of_questions=quiz_form_data['number_of_questions'],
                                        max_score=overall_max_score,
                                        author=request.user,
                                        author_id=request.user.id,
                                        name_slug=quiz_slug)
            for form in formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
                overall_max_score += question.max_score
            quiz.max_score = overall_max_score
            quiz.save()
            del request.session['quiz_form_data']
            return redirect(reverse('quizapp:quizmaker'))
    else:
        formset = my_form_set()

    return render(request, 'quizapp/add_questions.html', {'formset': formset, "username": request.user.username})

