from .models import Email
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task
from decouple import config
from logs.services import log_mail
from django.core.exceptions import ObjectDoesNotExist


auth_sent_from = "accounts@sortedtree.com"


# @shared_task
def send_confirmation_mail(username: str, email: str, token: str):
    mail = Email.objects.get(title="confirmation")
    # body = mail.body.format(token=token, url=config('URL'))
    body = mail.body.format(username=username, token=token, url=config('CLIENT_URL'))
    status = send_mail(mail.subject, body, auth_sent_from, [email, ], fail_silently=False)
    log_details = {
        "mail": mail,
        "body": body,
        "recipient": email,
        "sent_from": auth_sent_from,
        "type": 'SR',
        "recipients": '',
        "comments": 'The confirmation is sent for the user',
        "mail_count": status,
        'status': 1
    }
    # breakpoint()
    if log_details['mail_count'] == 0:
        log_details['status'] = 0
    log_mail(log_details)


# @shared_task
def promotion_mail(email: str):
    mail = Email.objects.get(title="Promotion")
    email = email
    status = send_mail(mail.subject, mail.body, auth_sent_from, [email, ], fail_silently=False)
    log_details = {
        "mail": mail,
        "body": mail.body,
        "recipient": email,
        "sent_from": auth_sent_from,
        "type": 'SR',
        "recipients": '',
        "comments": 'The Promotion mail for individual user',
        "mail_count": status,
    }
    if log_details['mail_count'] == 0:
        log_details['status'] = 0
    log_details['status'] = 1
    log_mail(log_details)


# @shared_task
def promotion_mail_mass(email_list: list, title: str):
    try:
        mail = Email.objects.get(title=title)
        b = []
        for email in email_list:
            b.append((mail.subject, mail.body, auth_sent_from, [email, ]))
        status = send_mass_mail(b, fail_silently=False)
        log_details = {
            "mail": mail,
            "body": mail.body,
            "recipient": email,
            "sent_from": auth_sent_from,
            "type": 'SR',
            "recipients": email_list,
            "comments": 'The Promotion mail for all the users is sent',
            "mail_count": status,
        }
        if log_details['mail_count'] == 0:
            log_details['status'] = 0
        log_details['status'] = 1
    except ObjectDoesNotExist:
        log_details = dict(comments="Something went wrong while sending the mail, check if mail exists in the db")
    log_mail(log_details)


# @shared_task
def send_password_reset_link(email: str, token: str):
    mail = Email.objects.get(title="passwordresetlink")
    body = mail.body.format(token=token, url=config('CLIENT_URL'))
    send_mail(mail.subject, body, auth_sent_from, [email, ], fail_silently=False)
