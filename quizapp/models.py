from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


class User(AbstractUser):
    USER_CHOICES = (
        (1, 'quiz taker'),
        (2, 'quiz maker')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_CHOICES, default=1)

    def __str__(self):
        return self.username


class QuizTaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class QuizMaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Quiz(models.Model):
    number_of_questions = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    topic = models.CharField(max_length=250)
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.TextField(max_length=5000)
    image = models.ImageField()
    max_score = models.PositiveIntegerField()
    correct_answer = models.TextField(max_length=200)
    incorrect_answer_1 = models.TextField(max_length=200)
    incorrect_answer_2 = models.TextField(max_length=200)
    incorrect_answer_3 = models.TextField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.str(id)

class QuizInstance(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_maker = models.ForeignKey(User, on_delete=models.CASCADE,related_name='quiz_author')
    max_score = models.IntegerField()
    actual_score = models.IntegerField()
    quiz_taker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz_id.name+" by " +self.quiz_maker.username

class QuestionInstance(models.Model):
    quiz_instance_id = models.ForeignKey(QuizInstance, on_delete=models.CASCADE)
    max_score = models.IntegerField()
    actual_score = models.IntegerField()

    def __str__(self):
        return self.id