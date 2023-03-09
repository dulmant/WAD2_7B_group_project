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
    TOPICS = (
        ("Java","Java"),
        ("Algorithms","Algorithms"),
        ("Web App Development","Web App Development"),
    )
    name = forms.CharField(max_length=250, label="Please enter the name of your quiz:")
    topic = forms.ChoiceField(label="Please choose the topic of your quiz", choices = TOPICS)
    number_of_questions = forms.IntegerField(initial=1, label="Please enter the number of questions:",min_value=1)
    name_slug = forms.CharField(widget=forms.HiddenInput, required=False)
    
    class Meta:
        model = Quiz
        fields = ('name','number_of_questions','topic')


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(max_length=5000, label="Please enter the question:", required=True)
    image = forms.ImageField(label="Image:", required=False)
    correct_answer = forms.CharField(max_length=200, label="Please enter the correct answer:", required=True)
    incorrect_answer_1 = forms.CharField(max_length=200, label="Please enter the first incorrect answer:")
    incorrect_answer_2 = forms.CharField(max_length=200, label="Please enter the second incorrect answer:")
    incorrect_answer_3 = forms.CharField(max_length=200, label="Please enter the third incorrect answer:")
    max_score = forms.IntegerField(initial=1, label="Please enter the available points for this question:",min_value=1)

    class Meta:
        model = Question
        fields = ('question_text', 'image', 'correct_answer',
                  'incorrect_answer_1', 'incorrect_answer_2', 'incorrect_answer_3','max_score')

class QuestionInstanceForm(forms.ModelForm):
    class Meta:
        model = QuestionInstance
        fields = ('answer_choice',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer_choice'].widget = forms.RadioSelect(choices=[], attrs={'class': 'form-check-input'})

    def set_choices(self, choices):
        self.fields['answer_choice'].choices = choices


class QuizInstanceForm(forms.ModelForm):
    max_score = forms.IntegerField()
    actual_score = forms.IntegerField()

    class Meta:
        model = QuizInstance
        fields = ('max_score', 'actual_score')
