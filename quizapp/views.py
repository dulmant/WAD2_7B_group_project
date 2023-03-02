from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import *

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

def quiz(request):
    return render(request, 'quizapp/quiz.html')

def about(request):
    return render(request, 'quizapp/about.html')

def contact(request):
    return render(request, 'quizapp/contact.html')

def quiz_maker_dashboard(request):
    return render(request, 'quizapp/quizmaker.html')

def quiz_taker_dashboard(request):
    return render(request, 'quizapp/quiztaker.html')
