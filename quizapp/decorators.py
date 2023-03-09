from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def quiz_taker_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_type == 1, #quiztaker
        login_url=reverse_lazy('index')
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def quiz_maker_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.user_type == 2, #quizmaker
        login_url=reverse_lazy('index')
    )
    if function:
        return actual_decorator(function)
    return actual_decorator