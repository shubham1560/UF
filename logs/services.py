from .models import SysEmailLog


def log_mail(log_details):
    print(log_details)
    log = SysEmailLog()
    log.status = log_details["status"]
    log.mail_sent_number = log_details["mail_count"]
    log.recipient = log_details["recipient"]
    log.recipients = log_details["recipients"]
    log.email = log_details["mail"]
    log.sent_from = log_details["sent_from"]
    log.email_body = log_details["body"]
    log.type = log_details["type"]
    log.comments = log_details["comments"]
    log.save()

