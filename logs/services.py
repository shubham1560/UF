from .models import SysEmailLog, RequestLog, RandomLog
import time
from django.core.exceptions import FieldDoesNotExist
from uFraudApi.settings.base import RANDOM_LOG, EMAIL_LOG, REQUEST_LOG


def log_mail(log_details):
    if EMAIL_LOG:
        try:
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
        except FieldDoesNotExist:
            pass


def log_request(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        total_time = time.time()-start_time
        if REQUEST_LOG:
            function_obj = str(func).split(" ")[1].split('.')
            try:
                req_log = RequestLog()
                req_log.viewset = function_obj[0]
                req_log.method = function_obj[1]
                req_log.status = f.status_text
                req_log.function = func
                req_log.time_elapsed = total_time
                req_log.request_body = args[1].data
                req_log.response_data = f.data
                req_log.save()
            except FieldDoesNotExist:
                pass
        return f
    return wrapper


def log_random(message: str, source: str = 'shubham'):
    print(RANDOM_LOG)
    if RANDOM_LOG:
        log = RandomLog()
        log.message = message
        log.source = source
        log.save()




