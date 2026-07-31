from django.utils.translation import gettext_lazy as _
from loguru import logger
from core_apps.accounts.models import BankAccount
from core_apps.user_auth.emails import _send_email
from django.conf import  settings

def send_suspicious_activity_alert(suspicious_activities):
    email = _send_email(
        _("Suspicious Activities"),
        settings.ADMIN_EMAIL,
        {
            "site_name": settings.SITE_NAME ,
            "suspicious_activities": suspicious_activities ,

        },
        "emails/suspicious_activity_alert.html"
    )

    try:
        email.send()
        logger.info(f"Suspicious Activities email has been sent successfully to ({settings.ADMIN_EMAIL}) : total suspicious_activities is: {len(suspicious_activities)} ")
        return len(suspicious_activities)

    except Exception as e:
        logger.error(f"Failed to sent Suspicious Activities email: ({settings.ADMIN_EMAIL}) : total suspicious_activities is: {len(suspicious_activities)} the ERROR : {str(e)}")

        return 0


def send_transfer_email(
        sender_email,
        receiver_email,
        sender_name,
        receiver_name,
        amount,
        currency,
        sender_new_balance,
        receiver_new_balance,
        sender_account_number,
        receiver_account_number
):

    context = {

            "site_name": settings.SITE_NAME ,
            "amount": amount,
            "currency": currency,
            "sender_account_number": sender_account_number   ,
            "receiver_account_number": receiver_account_number,
        }

    sender_context = {
        **context,
        "user": sender_name,
        "is_sender": True,
        "new_balance": sender_new_balance,
    }
    receiver_context = {
        **context,
        "user": receiver_name,
        "is_sender": False,
        "new_balance": receiver_new_balance,
    }

    sender_email = _send_email(
        _("Transfer Notification"),
        sender_email,
        sender_context,
        "emails/transfer_notification.html"
    )

    try:
        sender_email.send()
        logger.info(f"Transfer Notification email sender has been sent successfully to ({sender_email})")

    except Exception as e:
        logger.error(f"Failed to sent Transfer Notification sender email: ({sender_email}) and account_number: ({sender_account_number}) the ERROR : {str(e)}")

    receiver_email = _send_email(
        _("Transfer Notification"),
        receiver_email,
        receiver_context,
        "emails/transfer_notification.html"
    )

    try:
        receiver_email.send()
        logger.info(f"Transfer Notification receiver  email  has been sent successfully to ({receiver_email})")

    except Exception as e:
        logger.error(f"Failed to sent Transfer Notification receiver email: ({receiver_email}) and account_number: ({receiver_account_number}) the ERROR : {str(e)}")

def send_transfer_otp_email(email, otp):
    email = _send_email(
        _("Your OTP for transfer Authorization"),
        email,
        {
            "site_name": settings.SITE_NAME,
            "otp":otp,
            "expire_time": settings.OTP_EXIRATION
        },
        "emails/transfer_otp_email.html"
    )

    try:
        email.send()
        logger.info(f"OTP Transfer email has been sent successfully to ({email})")

    except Exception as e:
        logger.error(f"Failed to sent OTP transfer email: ({email}) and the ERROR : {str(e)}")

def send_withdrawal_email(user, user_email, amount, currency, new_balance, account_number):
    email = _send_email(
        _("Withdrawal Conformation"),
        user_email,
        {
            "user":user,
            "site_name": settings.SITE_NAME ,
            "amount": amount,
            "currency": currency,
            "new_balance": new_balance,
            "account_number": account_number,
        },
        "emails/withdrawal_conformation.html"
    )

    try:
        email.send()
        logger.info(f"Withdrawal Conformation  email has been sent successfully to ({user.email})")

    except Exception as e:
        logger.error(f"Failed to sent Withdrawal Conformation email: ({user_email}) and account_number: ({account_number}) the ERROR : {str(e)}")


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