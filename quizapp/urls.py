from django.urls import path
from quizapp import views

app_name = 'quizapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'), 
    # path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('quiz_taker_dashboard/', views.quiz_taker_dashboard, name='quiztaker'),
    path('quiz_maker_dashboard/', views.quiz_maker_dashboard, name='quizmaker'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('add_questions/<slug:quiz_slug>/<int:number_of_questions>', views.add_questions, name='add_questions'),
    # path('view_scores/', views.view_scores, name='view_scores'),
    # path('view_quizzes/', views.view_quizzes, name='view_quizzes'),
    path('quiz', views.quiz, name='quiz'),
    # path('quiz_success/', views.quiz_success, name='quiz_success'),
]
