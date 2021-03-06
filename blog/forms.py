from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email"
        self.fields['message'].label = "What can I help you with?"
        self.fields['captcha'].label = ""
