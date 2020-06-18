from .models import Email
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task
from decouple import config
from django.utils.html import strip_tags
from django.template.loader import render_to_string

sent_from = "Urbanfrauds@urbanfrauds.com"


@shared_task
def send_confirmation_mail(email: str, token: str):
    mail = Email.objects.get(title="confirmation")
    body = mail.body.format(token=token, url=config('URL'))
    send_mail(mail.subject, body, sent_from, [email, ], fail_silently=False)


@shared_task
def promotion_mail(email: str):
    mail = Email.objects.get(title="Promotion")
    email = email
    send_mail(mail.subject, mail.body, sent_from, [email, ], fail_silently=False)


@shared_task
def promotion_mail_mass(email_list: list):
    breakpoint()
    mail = Email.objects.get(title="Promotion")
    b = []
    for email in email_list:
        b.append((mail.subject, mail.body, sent_from, [email, ]))
    send_mass_mail(b, fail_silently=False)

