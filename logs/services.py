from .models import SysEmailLog, RequestLog
import time
from django.core.exceptions import FieldDoesNotExist


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


def log_request(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        total_time = time.time()-start_time
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
            print(req_log.id)
            # f.data[0] = req_log.id
        except FieldDoesNotExist:
            pass
        return f
    return wrapper



