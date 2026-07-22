from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedModel

User = get_user_model()

class BankAccount(TimeStampedModel):
    class AccountType(models.TextChoices):
        CURRENT = ("current", _("Current"))
        SAVING = ("saving", _("Saving"))

    class AccountStatus(models.TextChoices):
        ACTIVE = ("active", _("Active"))
        INACTIVE = ("inactive", _("Inactive"))


    class AccountCurrency(models.TextChoices):
        DOLLAR = ("us_dollar", _("US Dollar"))
        TOMAN = ("toman", _("Toman"))
        EURO = ("euro", _("Euro"))


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_account", verbose_name=_("User"))
    account_number = models.CharField(_("Account Number"), max_length=20, unique=True)
    account_balance = models.DecimalField(_("Account Balance"), decimal_places=2, max_digits=50, default=0.00)
    currency = models.CharField(_("Currency"), max_length=20, choices=AccountCurrency.choices, default=AccountCurrency.TOMAN)
    account_status = models.CharField(_("Account Status"), choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    account_type = models.CharField(_("Account Type"), choices=AccountType.choices, default=AccountType.SAVING)
    is_primary = models.BooleanField(_("Primary Account"), default=False)
    kyc_submitted = models.BooleanField(_("KYC Subbmitted"), default=False)
    kyc_verified = models.BooleanField(_("KYC Verified"), default=False)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verified_accounts", null=True, blank=True)
    verification_date = models.DateTimeField(_("Verification Date"), null=True, blank=True)
    verification_notes = models.CharField(_("Verification notes"), null=True, blank=True)
    fully_activated = models.BooleanField(_("Fully Activated"), default=False)

    def __str__(self) -> str:
        return f"{self.user.full_name}'s {self.get_currency_display()} - {self.get_account_type_display()} Account - {self.account_number}"

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")
        unique_together = ["user", "currency", "account_type"]

    def clean(self)->None:
        if self.account_balance < 0:
            raise ValidationError(_("Account balance can not be negative "))

    def save(self, *args, **kwargs) -> None:
        if self.is_primary:
            BankAccount.objects.filter(user=self.user).update(is_primary=False)
        
        super().save(*args, **kwargs)

class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PENDING = ("pending", _("Pending"))
        COMPLETED = ("completed", _("Completed"))
        FAILED = ("failed", "Failed")

    class TransactionType(models.TextChoices):
        DEPOSIT = ("deposit", _("Deposit"))
        WITHDRAWAL = ("withdrawal", _("Withdrawal"))
        TRANSFER = ("transfer", _("Transfer"))

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="transactions")
    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=30, default=0.00)
    description = models.CharField(_("Description"), max_length=500, null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="receiver_transactions")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sender_transactions")
    receiver_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name="receiver_transactions")
    sender_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name="sender_transactions")
    status = models.CharField(_("Transaction Status"), choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    transaction_type = models.CharField(_("Transaction Type"), choices=TransactionType.choices, default=TransactionType.TRANSFER)


    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.amount} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]


