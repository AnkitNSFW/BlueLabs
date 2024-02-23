from django.contrib.sessions.models import Session
from django.utils import timezone

import sys
sys.path.append('')
from utility.email_functions.email_notification import send_email
from utility.utility_func import current_DT
from app.models import OTP


def cron_jobs_manager(request):
    # deleteing all the Expired Sessions
    clear_expired_sessions()
    # Deleting all the expired OTP's
    delete_expired_otps()


def clear_expired_sessions():
    current_time = timezone.now()
    all_session_count = Session.objects.count()
    expired_sessions = Session.objects.filter(expire_date__lt=current_time)
    expired_session_count = expired_sessions.count()
    valid_session_count = all_session_count - expired_session_count
    expired_sessions.delete()
    if expired_session_count:
        subject = f'Deleted {expired_session_count} expired Sessions from DB.'
        message = f"""
        Successfully deleted {expired_session_count} expired session(s).
        
        All the expired Session with respect to time {current_time} were deleted.
        Their are {valid_session_count} Valid Sessions in DB
        """
        send_email(subject=subject, content=message, to_addr='ankit141003@gmail.com')

def delete_expired_otps():
    OTP.objects.filter(valid_till__lt=current_DT()).delete()