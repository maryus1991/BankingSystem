
from django.conf import settings
from core_apps.user_auth.emails import _send_email
from django.utils.translation import gettext_lazy as _
from loguru import logger

def send_virtual_card_topup_email(user, virtual_card, amount, new_balance):

    email = _send_email(
        _("Virtual Card Top-Up Conformation"),
        user.email,
        {
            "user_full_name": user.full_name,
            "card_last_four": virtual_card.card_number[-4:],
            "amount": amount,
            "new_balance": new_balance,
            "currency": virtual_card.bank_account.currency,
            "site_name": settings.SITE_NAME
        },
        "emails/virtual_card_topup.html"
    )

    try:
        email.send()
        logger.info(
            "Virtual card topup email sent to {}".format(user.email)
        )
    except Exception as e:
        logger.error(
            "Virtual card topup email failed sent to {} and error : {}".format(user.email, e)
        )
