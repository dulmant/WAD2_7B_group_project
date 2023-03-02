from django import forms
from .models import *


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label="Please enter a username:", required=True)
    password = forms.CharField(max_length=30, label="Please enter a password:", required=True, widget=forms.PasswordInput())
    email = forms.EmailField(label="Please enter an email.", required=True)
    user_type = forms.ChoiceField(initial=0, label = "Would you like to register as a quiz taker or quiz maker?",choices = User.USER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'user_type')


class QuizForm(forms.ModelForm):
    number_of_questions = forms.IntegerField(initial=1, help_text="Please enter the number of questions:")
    max_score = forms.IntegerField(initial=0, help_text="Please enter the max score:")
    topic = forms.CharField(max_length=50, help_text="Please enter the topic:")

    class Meta:
        model = Quiz
        fields = ('number_of_questions', 'max_score', 'topic')


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(max_length=5000, help_text="Please enter the question:", required=True)
    image = forms.ImageField(help_text="Image:", required=False)
    correct_answer = forms.CharField(max_length=200, help_text="Please enter the correct answer:", required=True)
    incorrect_answer_1 = forms.CharField(max_length=200, help_text="Please enter the first incorrect answer:")
    incorrect_answer_2 = forms.CharField(max_length=200, help_text="Please enter the second incorrect answer:")
    incorrect_answer_3 = forms.CharField(max_length=200, help_text="Please enter the third incorrect answer:")

    class Meta:
        model = Question
        fields = ('question_text', 'image', 'correct_answer',
                  'incorrect_answer_1', 'incorrect_answer_2', 'incorrect_answer_3')


class QuizInstanceForm(forms.ModelForm):
    max_score = forms.IntegerField()
    actual_score = forms.IntegerField()

    class Meta:
        model = QuizInstance
        fields = ('max_score', 'actual_score')


class QuizInstanceForm(forms.ModelForm):
    max_score = forms.IntegerField()
    actual_score = forms.IntegerField()

    class Meta:
        model = QuizInstance
        fields = ('max_score', 'actual_score')
