from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core_apps.accounts.models import BankAccount
from core_apps.common.models import TimeStampedModel

User = get_user_model()


class VirtualCard(TimeStampedModel):
    class CardStatus(models.TextChoices):
        ACTIVE = ("active", _("Active"))
        INACTIVE = ("inactive", _("Inactive"))
        BLOCK = ("block", _("Block"))


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="virtual_cards")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="virtual_cards")
    card_number = models.CharField(max_length=16, unique=True, db_index=True)
    expiry_date = models.DateTimeField()
    cvv = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=CardStatus.choices, default=CardStatus.ACTIVE)

    def __str__(self):
        return "Virtual Card {} for {}".format(self.card_number, self.user.full_name)