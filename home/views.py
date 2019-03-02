from django.contrib import messages
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
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(data=request.POST)

        contact_name = request.POST.get('contact_name', "")
        contact_email = request.POST.get('contact_email', "")
        subject = request.POST.get('subject', "")
        message = request.POST.get('message', "")

        if form.is_valid():
            email_template = get_template('home/contact_template.txt')

            email_context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_message': message,
            }
            email_content = email_template.render(email_context)

            with mail.get_connection() as connection:
                email = mail.EmailMessage(
                    f"Contact Form Submission: {subject}",
                    email_content,
                    'Contact Form <contact@mg.danhayes.dev>',
                    ['dan@danhayes.dev', ],
                    reply_to=[contact_email, ],
                    connection=connection
                )
                sent = email.send()
                if sent == 1:
                    messages.info(request, "Thank you, the email was sent.")
                else:
                    messages.error(request,
                                   "There seems to have been a problem sending the email. Please try again later.")

            return redirect('home:home')
        else:
            form = ContactForm(data=request.POST)

    context = {'blurbs': blurbs,
               'form': form}
    return render(request, 'home/index.html', context)


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', "")
            contact_email = request.POST.get('contact_email', "")
            subject = request.POST.get('subject', "")
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
                    f"Contact Form Submission: {subject}",
                    content,
                    'Contact Form <contact@mg.danhayes.dev>',
                    ['daniel@danhayes.dev', ],
                    reply_to=[contact_email, ],
                    connection=connection
                ).send()

            return redirect('home:home')

    context = {'form': form_class}
    return render(request, 'home/contact.html', context)
