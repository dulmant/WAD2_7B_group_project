from django.urls import path
from quizapp import views

app_name = 'quizapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'), 
    path('logout/', views.user_logout, name='logout'),
    path('quiz_taker_dashboard/', views.quiz_taker_dashboard, name='quiztaker'),
    path('quiz_maker_dashboard/', views.quiz_maker_dashboard, name='quizmaker'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('add_questions/<slug:quiz_slug>/<int:number_of_questions>', views.add_questions, name='add_questions'),
    path('quiz/<slug:quiz_slug>/', views.quiz, name='quiz'),
    path('view_other_quizzes/', views.view_other_quizzes, name='view_other_quizzes'),
    path('quiz_finish/<slug:quiz_slug>/', views.quiz_finish, name='quiz_finish'),
    path('ajax/delete_quiz/<slug:quiz_slug>/', views.ajax_delete_quiz, name='ajax_delete_quiz'), 
    path('view_quiz/<slug:quiz_slug>/', views.view_quiz, name='view_quiz'), 
] 

