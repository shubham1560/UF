from .models import Email
from django.core.mail import send_mail
from celery import shared_task
from decouple import config
from django.utils.html import strip_tags
from django.template.loader import render_to_string

html_message = "<b>Well the html message</b>"
plain_message = strip_tags(html_message)


@shared_task
def send_confirmation_mail(email: str, token: str):
    mail = Email.objects.get(title="confirmation")
    body = mail.body.format(token=token, url=config('URL'))
    sent_from = "Urbanfrauds@urbanfrauds.com"
    send_mail(mail.subject, plain_message, sent_from, [email, ], fail_silently=False, html_message="<b>Html</b>")
