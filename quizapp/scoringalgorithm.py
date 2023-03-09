def score_question(question, truefalse):
    if truefalse:
        return question.max_score
    else:
        return 0


def score_quiz(scores):
    total = 0
    for score in scores:
        total += score
    return total
