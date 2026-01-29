EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smpt.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ab2754315@gmail.com'
EMAIL_HOST_PASSWORD = 'uwil kkmy dorh komh'
DEFAULT_FROM_EMAIL = 'ab2754315@gmail.com'


from django.core.mail import send_mail

def send_simple_email(request, user_email):
    subject = 'Tasdiqlash kodi'
    message = 'Sizning kodingiz: 12412421'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user_email,]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print("Email sent successfully!")


send_simple_email('ab2754315@gmail.com')
