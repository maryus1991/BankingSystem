from django.utils.translation import gettext_lazy as _
from loguru import logger
from celery import shared_task

from django.conf import settings
from core_apps.user_auth.emails import _send_email



def send_account_creation_email(user, bank_account):


    email = _send_email(
        _("Your New Bank Account has been Created "),
        user.email,
        {
            "user":user,
            "site_name": settings.SITE_NAME ,
            "account": bank_account,
        },
        "emails/account_created.html"
    )

    try:
        email.send()
        logger.info(f"Account Creation email has been sent successfully to ({user.email})")

    except Exception as e:
        logger.error(f"Failed to sent Account Creation email ({user.email}) and ({bank_account}) the ERROR : {str(e)}")