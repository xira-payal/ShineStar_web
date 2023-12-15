from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_forgot_password_email(email, token_b64):
    subject = 'Your Forgot Password Link'
    token_b64 = urlsafe_base64_encode(force_bytes(token_b64))
    message = f'Hi, Click On the Link to Reset Your Password http://127.0.0.1:8000/admin/resetPassword/{token_b64}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

