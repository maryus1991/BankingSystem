from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger

def send_otp_email(email, otp):
    subject = _('Your OTP code for Login')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        'otp': otp,
        'expire_time':settings.OTP_EXPIRE_TIME,

    }

    html_email = render_to_string('emails/otp_email.html', context)
    plain_email = strip_tags(html_email)
    msg = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    msg.attach_alternative(html_email, "text/html")

    try:
        email.send()
        logger.info(f"Email sent successfully to : {email}")
    except Exception as error:
        logger.error(f"Failed send OTP email to {email} and got ERROR {str(error)}")


def send_account_locked_email(self):
    subject = _('Your account has been locked')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [self.email]
    context = {
        'user': self,
        'lockout_duration': int(settings.LOCK_OUT_DURATION.total_seconds() // 60),

    }

    html_email = render_to_string('emails/account_locked.html', context)
    plain_email = strip_tags(html_email)
    msg = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    msg.attach_alternative(html_email, "text/html")

    try:
        email.send()
        logger.info(f"Account lock email sent successfully to : {self.email}")
    except Exception as error:
        logger.error(f"Failed send account lock email to {self.email} and got ERROR {str(error)}")