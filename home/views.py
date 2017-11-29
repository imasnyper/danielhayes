from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

from .forms import ContactForm
from .models import Blurb

from .utils import gmail_backend


# Create your views here.
def index(request):
    blurbs = Blurb.objects.order_by("order_num")
    blurbs = [blurbs[i:i+3] for i in range(0, len(blurbs), 3)]
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', "")
            contact_email = request.POST.get('contact_email', "")
            message = request.POST.get('message', "")

            template = get_template('home/contact_template.txt')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_message': message,
            }
            content = template.render(context)

            service = gmail_backend.set_up()
            email = gmail_backend.create_message(
                'webmaster@dhayes.me', 
                'daniel@dhayes.me',
                "New Contact Form Submission from {}".format(contact_email),
                content,
                contact_email,
            )
            sent = gmail_backend.send_message(service, 'daniel@dhayes.me' , email)
            return redirect('home:home')

    context = {'blurbs': blurbs,
               'form': form_class}
    return render(request, 'home/index.html', context)


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', "")
            contact_email = request.POST.get('contact_email', "")
            message = request.POST.get('message', "")

            template = get_template('home/contact_template.txt')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_message': message,
            }
            content = template.render(context)

            service = gmail_backend.set_up()
            email = gmail_backend.create_message(
                'daniel@dhayes.me', 
                'danihaye@gmail.com',
                "New Contact Form Submission from {}".format(contact_email),
                content,
            )
            sent = gmail_backend.send_message(service, 'daniel@dhayes.me' , email)
            return redirect('home:home')

    context = {'form': form_class}
    return render(request, 'home/contact.html', context)

# from django.shortcuts import render, get_list_or_404, get_object_or_404
# from django.utils import timezone
#
# from polls.models import Question
#
# import datetime
#
# # Create your views here.
# def index(request):
#     last_question = []
#     active_questions = []
#     last_question = Question.objects.filter(expiry_date__lte=timezone.now())[0]
#     active_questions = Question.objects.filter(expiry_date__gt=timezone.now())
#     context = {'last_question': last_question,
#                'active_questions': active_questions,}
#     return render(request, 'home/index_old.html', context)