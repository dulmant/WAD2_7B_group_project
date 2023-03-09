from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from .decorators import *


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
        return render(request, 'quizapp/index.html', {'username':request.user.username})

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
            messages.success(request, "Registration successful." )
            registered = True
            return redirect(reverse('quizapp:index'))
        else:
            print(form.errors)
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:

        form = UserForm()

    return render(request,
                'quizapp/register.html',
                context = {'form': form,
                        'registered': registered})


def user_logout(request):
    logout(request)
    return redirect(reverse('quizapp:index'))

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.forms import formset_factory
from .models import Quiz, Question

@quiz_taker_required
def quiz(request, quiz_slug):
    quiz_instance = get_object_or_404(Quiz, name_slug=quiz_slug)
    number_of_questions = quiz_instance.number_of_questions

    questions = Question.objects.filter(quiz=quiz_instance)

    question_options = []
    for question in questions:
        # add options to question_options list
        options = [question.correct_answer, question.incorrect_answer_1, question.incorrect_answer_2, question.incorrect_answer_3]
        question_options.append([question, options])

    context = {
        'quiz': quiz_instance,
        'questions': questions,
        'number_of_questions': number_of_questions,
        'quiz_instance': quiz_instance,
        'question_options': question_options
    }
    return render(request, 'quizapp/quiz.html', context)

def about(request):
    return render(request, 'quizapp/about.html')

def contact(request):
    return render(request, 'quizapp/contact.html')

@quiz_maker_required
def quiz_maker_dashboard(request):
    has_quizzes=False
    if Quiz.objects.filter(author=request.user).exists():
        has_quizzes=True
    my_quizzes = Quiz.objects.filter(author=request.user)
      
    context={'my_quizzes':my_quizzes,'has_quizzes':has_quizzes}
    return render(request, 'quizapp/quizmaker.html', context)

@quiz_taker_required
def quiz_taker_dashboard(request):
    quizzes_exist=False
    if Quiz.objects.all().exists():
        quizzes_exist=True
    all_quizzes = Quiz.objects.all()
      
    context={'all_quizzes':all_quizzes,'quizzes_exist':quizzes_exist}
    return render(request, 'quizapp/quiztaker.html', context)

@quiz_maker_required
def create_quiz(request):
    if request.method == 'POST':
        form=QuizForm(request.POST)
        if form.is_valid():
            form.instance.max_score=form.instance.number_of_questions
            form.instance.author = request.user
            form.instance.author_id = request.user.id
            form.instance.name_slug = slugify(form.instance.name)
            form.save()
            return redirect(reverse('quizapp:add_questions',kwargs={'quiz_slug': form.instance.name_slug,'number_of_questions':form.instance.number_of_questions}))
    context={ "form" : QuizForm, "username" : request.user.username }
    
    return render(request, 'quizapp/create_quiz.html', context)

@quiz_maker_required
def add_questions(request,quiz_slug, number_of_questions):
    MyFormSet = formset_factory(QuestionForm, extra=number_of_questions)
    if request.method == 'POST':
        formset = MyFormSet(request.POST)
        if formset.is_valid():
            overall_max_score=0
            for form in formset:
                form.instance.quiz=Quiz.objects.get(name_slug=quiz_slug)
                form.instance.quiz_id=Quiz.objects.get(name_slug=quiz_slug).id
                form.save()
                overall_max_score+=form.instance.max_score
            Quiz.objects.update_or_create(name_slug = quiz_slug, defaults={'max_score':overall_max_score})
            return redirect(reverse('quizapp:quizmaker'))
    else:
        formset = MyFormSet()
    return render(request, 'quizapp/add_questions.html', {'formset': formset, "username" : request.user.username })