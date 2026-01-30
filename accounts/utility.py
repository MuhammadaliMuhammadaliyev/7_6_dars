import re

from braintree.validation_error import ValidationError
from django.core.mail import send_mail
from django.conf import settings



def send_simple_email(user_email, code):
    subject = 'Tastiqlash kodingiz!'
    message = f'Sizning tastiqlash kodingiz: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    return True


email_regex = re.compile(r"/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/")

def check_email(email):
    if re.fullmatch(email_regex, email):
        email = True
    else:
        raise ValidationError('Email xato kiritilgan')

    return email