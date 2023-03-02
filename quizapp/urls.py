from django.urls import path
from quizapp import views

app_name = 'quizapp'

urlpatterns = [
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'), 
    # path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('quiz_taker_dashboard/', views.quiz_taker_dashboard, name='quiz_taker_dashboard'),
    # path('quiz_maker_dashboard/', views.quiz_maker_dashboard, name='quiz_maker_dashboard'),
    # path('add_quiz/', views.add_quiz, name='add_quiz'),
    # path('view_scores/', views.view_scores, name='view_scores'),
    # path('view_quizzes/', views.view_quizzes, name='view_quizzes'),
    # path('quiz/<int:page_id>', views.quiz, name='quiz'),
    # path('quiz_success/', views.quiz_success, name='quiz_success'),
]
