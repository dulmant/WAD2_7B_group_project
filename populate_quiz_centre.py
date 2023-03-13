import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','QuizCentre.settings')

import django
django.setup()
from quizapp.models import User, Quiz, Question

def populate():

    user_cale = [
        {'username': 'cale001', 'password': 'password1', 'email': 'cale@cale.com', 'user_type': 2},
        {'username': 'j0hns0n', 'password': 'password2', 'email': 'john@theJohnsons.co.uk', 'user_type': 1}
    ]

    for u in user_cale:
        add_user(u['username'], u['password'], u['email'], u['user_type'])



    quizes = [
        {'number_of_questions': '1', 'max_score': 1, 'topic': 'Veterinary', 'name': 'Veterinary quiz 1',
         'author': User.objects.get(username='cale001'),
         'name_slug': 'VeterinaryQuiz1'},

        {'number_of_questions': '3', 'max_score': 6, 'topic': 'Mathematics', 'name': 'Simple Mathematics Introduction',
         'author': User.objects.get(username='cale001'),
         'name_slug': 'SimpleMathematicsIntroduction'},

        {'number_of_questions': '2', 'max_score': 6, 'topic': 'Web App Development', 'name': 'Website',
         'author': User.objects.get(username='cale001'),
         'name_slug': 'website'},

        {'number_of_questions': '1', 'max_score': 1, 'topic': 'English', 'name': 'Introduction to Punctuation',
         'author': User.objects.get(username='cale001'),
         'name_slug': 'IntroductionToPunctuation'},
    ]


    for q in quizes:
        add_quiz(q['name'], q['number_of_questions'], q['max_score'], q['topic'],
                 q['author'], q['name_slug'])



    cats_quiz_questions = [
        {'question_text': 'Do cats have tails?', 'image': '', 'max_score': 1,
         'correct_answer': 'yes', 'incorrect_answer_1': 'all of the above', 'incorrect_answer_2': 'no',
         'incorrect_answer_3': 'maybe', 'quiz': Quiz.objects.get(name_slug='VeterinaryQuiz1')}
    ]

    maths_quiz_questions = [
        {'question_text': 'What is 2+2?', 'image': '', 'max_score': 2,
         'correct_answer': '4', 'incorrect_answer_1': '3', 'incorrect_answer_2': '-4',
         'incorrect_answer_3': '5', 'quiz': Quiz.objects.get(name_slug='SimpleMathematicsIntroduction')},

        {'question_text': 'What is 5x5?', 'image': '', 'max_score': 2,
         'correct_answer': '25', 'incorrect_answer_1': '20', 'incorrect_answer_2': '-20',
         'incorrect_answer_3': '10', 'quiz': Quiz.objects.get(name_slug='SimpleMathematicsIntroduction')},

        {'question_text': 'What is -8/2?', 'image': '', 'max_score': 2,
         'correct_answer': '-4', 'incorrect_answer_1': '16', 'incorrect_answer_2': '4',
         'incorrect_answer_3': '8/2', 'quiz': Quiz.objects.get(name_slug='SimpleMathematicsIntroduction')}
    ]

    website_quiz_questions = [
        {'question_text': "Why isn't an image appearing", 'image': '', 'max_score': 2,
         'correct_answer': 'The question was setup without one', 'incorrect_answer_1': 'A bad internet connection',
         'incorrect_answer_2': 'The image is displayed correctly',
         'incorrect_answer_3': 'An incorrect image url was used', 'quiz': Quiz.objects.get(name_slug='website')},

        {'question_text': 'Is this a good website?', 'image': '', 'max_score': 4,
         'correct_answer': 'Absolutely!', 'incorrect_answer_1': 'meh', 'incorrect_answer_2': 'no',
         'incorrect_answer_3': "it's ok", 'quiz': Quiz.objects.get(name_slug='website')}
    ]

    english_quiz_questions = [
        {'question_text': 'Identify the comma', 'image': '', 'max_score': 1,
         'correct_answer': ',', 'incorrect_answer_1': '.', 'incorrect_answer_2': ';',
         'incorrect_answer_3': "'", 'quiz': Quiz.objects.get(name_slug='IntroductionToPunctuation')}
    ]

    # I realise this next part is repetitive, I'll be back to fix it
    for qu in cats_quiz_questions:
        add_question(qu['question_text'], qu['image'], qu['max_score'], qu['correct_answer'],
                     qu['incorrect_answer_1'], qu['incorrect_answer_2'], qu['incorrect_answer_3'], qu['quiz'])

    for qu in maths_quiz_questions:
        add_question(qu['question_text'], qu['image'], qu['max_score'], qu['correct_answer'],
                     qu['incorrect_answer_1'], qu['incorrect_answer_2'], qu['incorrect_answer_3'], qu['quiz'])

    for qu in website_quiz_questions:
        add_question(qu['question_text'], qu['image'], qu['max_score'], qu['correct_answer'],
                     qu['incorrect_answer_1'], qu['incorrect_answer_2'], qu['incorrect_answer_3'], qu['quiz'])

    for qu in english_quiz_questions:
        add_question(qu['question_text'], qu['image'], qu['max_score'], qu['correct_answer'],
                     qu['incorrect_answer_1'], qu['incorrect_answer_2'], qu['incorrect_answer_3'], qu['quiz'])



def add_user(username, password, email, user_type):
    # I have no idea why add_user doesn't work like add_quiz.

    u = User.objects.get_or_create(username=username,password=password,email=email,user_type=user_type)
    # u.username = username
    # u.password = password
    # u.email = email
    # u.user_type = user_type
    # u.save()
    return u
def add_question(question_text, image, max_score, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3, quizess):
    # Again I have no idea why.

    qu = Question.objects.get_or_create(question_text=question_text, max_score=max_score, quiz=quizess)[0]
    # qu.question_text = question_text
    qu.image = image
    # qu.max_score = max_score
    qu.correct_answer = correct_answer
    qu.incorrect_answer_1 = incorrect_answer_1
    qu.incorrect_answer_2 = incorrect_answer_2
    qu.incorrect_answer_3 = incorrect_answer_3
    # qu.quiz = quizess
    qu.save()
    return qu

def add_quiz(name, number_of_questions, max_score, topic, author, name_slug):
    q = Quiz.objects.get_or_create(name=name)[0]
    q.number_of_questions = number_of_questions
    q.max_score = max_score
    q.topic = topic
    q.author = author
    q.name_slug = name_slug
    q.save()
    return q



if __name__ == '__main__':
    print('Starting quiz app population script...')
    populate()
    print('Done :)')