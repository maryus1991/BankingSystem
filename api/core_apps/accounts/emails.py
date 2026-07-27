from django.utils.translation import gettext_lazy as _
from loguru import logger
from celery import shared_task
from core_apps.accounts.models import BankAccount
from django.conf import settings
from core_apps.user_auth.emails import _send_email



def send_deposit_email(user, user_email, amount, currency, new_balance, account_number):
    email = _send_email(
        _("Deposit Conformation"),
        user_email,
        {
            "user":user,
            "site_name": settings.SITE_NAME ,
            "amount": amount,
            "currency": currency,
            "new_balance": new_balance,
            "account_number": account_number,
        },
        "emails/deposit_conformation.html"
    )

    try:
        email.send()
        logger.info(f"Deposit Conformation  email has been sent successfully to ({user.email})")

    except Exception as e:
        logger.error(f"Failed to sent Deposit Conformation email: ({user_email}) and account_number: ({account_number}) the ERROR : {str(e)}")

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

def send_full_activation_email(account: BankAccount) -> None:
    email = _send_email(
        _("Your Bank Account is now fully activated "),
        account.user.email,
        {

            "site_name": settings.SITE_NAME ,
            "account": account,
        },
        "emails/bank_account_activated.html"
    )

    try:
        email.send()
        logger.info(f"Account Activation email has been sent successfully to ({account.user.email})")

    except Exception as e:
        logger.error(f"Failed to sent Account Activation email ({account.user.email}) and ({account}) the ERROR : {str(e)}")