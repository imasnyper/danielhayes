from django.core import mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from .models import Blurb


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

            with mail.get_connection() as connection:
                email = mail.EmailMessage(
                    f"New Contact Form Submission from {contact_email}",
                    content,
                    'do-not-reply@mg.dhayes.me',
                    ['daniel@dhayes.me', ],
                    reply_to=[contact_email, ],
                    connection=connection
                )
                email.send()

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

            with mail.get_connection() as connection:
                mail.EmailMessage(
                    f"New Contact Form Submission from {contact_email}",
                    content,
                    'do-not-reply@mg.dhayes.me',
                    ['daniel@dhayes.me', ],
                    reply_to=[contact_email, ],
                    connection=connection
                ).send()

            return redirect('home:home')

    context = {'form': form_class}
    return render(request, 'home/contact.html', context)
