from django import forms
from rango.models import User, QuizTaker, QuizMaker, Quiz, Question, QuizInstance, QuestionInstance


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text="Please enter a username:", required=True)
    password = forms.CharField(max_length=30, help_text="Please enter a password:", required=True)
    email = forms.EmailField(help_text="Please enter an email.", required=True)
    user_type = forms.PositiveSmallIntegerField(initial=0)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'user_type')


class QuizTakerForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text="Please enter a username:", required=True)
    password = forms.CharField(max_length=30, help_text="Please enter a password:", required=True)
    # user = forms.OneToOneField(User, help_text="Please enter the User:")

    class Meta:
        model = QuizTaker
        fields = ('username', 'password')


class QuizMakerForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text="Please enter a username:", required=True)
    password = forms.CharField(max_length=30, help_text="Please enter a password:", required=True)
    # user = forms.OneToOneField(User, help_text="Please enter the User:")

    class Meta:
        model = QuizMaker
        fields = ('username', 'password')


class QuizForm(forms.ModelForm):
    number_of_questions = forms.IntegerField(initial=1, help_text="Please enter the number of questions:")
    max_score = forms.IntegerField(initial=0, help_text="Please enter the max score:")
    topic = forms.CharField(max_length=50, help_text="Please enter the topic:")
    # author_id = forms.ForeignKey(User, help_text="Please enter the author ID:")

    class Meta:
        model = Quiz
        fields = ('number_of_questions', 'max_score', 'topic')


class QuestionForm(forms.ModelForm):
    question_text = forms.TextField(max_length=5000, help_text="Please enter the question:", required=True)
    image = forms.ImageField(help_text="Image:", required=False)
    correct_answer = forms.TextField(max_length=200, help_text="Please enter the correct answer:", required=True)
    incorrect_answer_1 = forms.TextField(max_length=200, help_text="Please enter the first incorrect answer:")
    incorrect_answer_2 = forms.TextField(max_length=200, help_text="Please enter the second incorrect answer:")
    incorrect_answer_3 = forms.TextField(max_length=200, help_text="Please enter the third incorrect answer:")
    # quiz_id = forms.ForeignKey(Quiz, help_text="Please enter the quiz ID:")

    class Meta:
        model = Question
        fields = ('question_text', 'image', 'correct_answer',
                  'incorrect_answer_1', 'incorrect_answer_2', 'incorrect_answer_3')


class QuizInstanceForm(forms.ModelForm):
    # quiz_id = forms.ForeignKey(Quiz, help_text="Please enter the quiz ID:")
    max_score = forms.IntegerField()
    actual_score = forms.IntegerField()
    # quiz_taker = forms.ForeignKey(QuizTaker, help_text="Please enter the quiz taker:")


    class Meta:
        model = QuizInstance
        fields = ('max_score', 'actual_score')


class QuizInstanceForm(forms.ModelForm):
    # quiz_instance_id = forms.ForeignKey(QuizInstance, help_text="Please enter the quiz instance ID:")
    max_score = forms.IntegerField()
    actual_score = forms.IntegerField()


    class Meta:
        model = QuizInstance
        fields = ('max_score', 'actual_score')
