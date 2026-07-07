from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def _send_email(subject, recipient_list, context, template):
    from_email = settings.DEFAULT_FROM_EMAIL
    html_email = render_to_string(template, context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_file(html_email, "text/html")

    return email


def send_otp_email(email_list, otp):
    subject = _("Your OTP code for Login")
    recipient_list = [email_list]
    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,

    }

    email = _send_email(subject, recipient_list, context, "emails/otp_email.html")

    try:
        email.send()
        logger.info(f"OTP email send successfully to {email_list}")

    except Exception as e:
        logger.error(f"Failed to send OTP email to {email_list} and the ERROR : {str(e)}")


def send_account_locked_email(self):
    subject = _("Your account has been locked")
    recipient_list = [self.email]
    context = {
        "user": self,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_secound() // 60),
        "site_name": settings.SITE_NAME,

    }

    email = _send_email(subject, recipient_list, context, "emails/account_locked.html")

    try:
        email.send()
        logger.info(f"Account locked email sent {self.email}")

    except Exception as e:
        logger.error(f"Failed to send account locked email to {self.email} and the ERROR: {str(e)}")
