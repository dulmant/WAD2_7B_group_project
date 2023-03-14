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

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='question_images', blank=True)
    max_score = models.PositiveIntegerField()
    correct_answer = models.TextField(max_length=200)
    incorrect_answer_1 = models.TextField(max_length=200)
    incorrect_answer_2 = models.TextField(max_length=200)
    incorrect_answer_3 = models.TextField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz.name + ": Question " + str(self.id)


class QuizInstance(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_author')

    def __str__(self):
        return self.quiz_id.name + " by " + self.quiz_maker.username


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_author')
    max_score = models.IntegerField()
    actual_score = models.IntegerField()
    quiz_taker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz.name + " by " + self.quiz_maker.username + str(self.id)


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_taker = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    max_score = models.IntegerField()
    actual_score = models.IntegerField()
    answer_choice = models.CharField(max_length=500)

    def __str__(self):
        return "answer by " + self.quiz_taker.username + " to question " + str(
            self.question.id) + " from quiz " + self.quiz.name
