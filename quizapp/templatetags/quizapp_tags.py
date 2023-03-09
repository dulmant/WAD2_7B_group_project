import random
from django import template

register = template.Library()

@register.filter
def shuffle(arg):
    """
    Shuffles a list in place and returns the shuffled list.
    """
    aux = arg.copy()
    random.shuffle(aux)
    return aux