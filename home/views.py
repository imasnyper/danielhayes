from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.utils import timezone

from polls.models import Question

# Create your views here.
def index(request):

    # last_question = Question.objects.filter(
    #         pub_date__lte=timezone.now()).order_by('-pub_date')[1]
    questions = get_list_or_404(Question, pub_date__lte=timezone.now())
    last_question = questions[1]
    last_question_total_votes = sum([choice.votes for choice in last_question.choice_set.all()])
    active_questions = get_list_or_404(Question, expiry_date__gt=timezone.now())
    context = {'last_question': last_question,
               'active_questions': active_questions,
               'last_question_total_votes': last_question_total_votes}
    return render(request, 'home/index.html', context)
