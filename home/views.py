from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.utils import timezone

from polls.models import Question

import datetime

# Create your views here.
def index(request):
    last_question = []
    active_questions = []
    last_question = Question.objects.filter(expiry_date__lte=timezone.now())[0]
    active_questions = Question.objects.filter(expiry_date__gt=timezone.now())
    context = {'last_question': last_question,
               'active_questions': active_questions,}
    return render(request, 'home/index.html', context)
