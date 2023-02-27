from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    user_type = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.username


class QuizTaker(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class QuizMaker(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Quiz(models.Model):
    number_of_questions = models.IntegerField()
    max_score = models.IntegerField()
    topic = models.CharField(max_length=50)
    author_id = models.ForeignKey(QuizMaker, on_delete=models.CASCADE)


class Question(models.Model):
    question_text = models.TextField(max_length=5000)
    image = models.ImageField()
    correct_answer = models.TextField(max_length=200)
    incorrect_answer_1 = models.TextField(max_length=200)
    incorrect_answer_2 = models.TextField(max_length=200)
    incorrect_answer_3 = models.TextField(max_length=200)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class QuizInstance(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    max_score = models.IntegerField()
    actual_score = models.IntegerField()
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)


class QuestionInstance(models.Model):
    quiz_instance_id = models.ForeignKey(QuizInstance, on_delete=models.CASCADE)
    max_score = models.IntegerField()
    actual_score = models.IntegerField()

