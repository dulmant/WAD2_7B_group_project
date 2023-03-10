from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
from django.forms import formset_factory

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

def quiz(request):
    return render(request, 'quizapp/quiz.html')

def about(request):
    return render(request, 'quizapp/about.html')

def contact(request):
    return render(request, 'quizapp/contact.html')

def quiz_maker_dashboard(request):
    my_quizzes = Quiz.objects.filter(author=request.user)
    context={'my_quizzes':my_quizzes}
    return render(request, 'quizapp/quizmaker.html', context)

def quiz_taker_dashboard(request):
    return render(request, 'quizapp/quiztaker.html')

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