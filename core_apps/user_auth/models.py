from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import uuid

from .emails import send_account_locked_email
from .managers import UserManager

class User(AbstractUser):
    class SecurityQuestion(models.TextChoices):
        GrandFatherName=(
            'grand_father_name', _('What is your Grand Father Name'),
        )
        FavoriteColor=(
            'favor_color', _('What is your favor color'),
        )
        BIRTH_CITY=(
            'birth_city', _('What is your birth city'),
        )
        CHILD_HOOD_FRIENDS=(
            'child_friends', _('What is your child friends name'),
        )

    class AccountStatus(models.TextChoices):
        ACTIVE=('active', _('Active'))
        LOCKED=('locked', _('Locked'))

    class RoleChoices(models.TextChoices):
        CUSTOMER=('customer', _('Customer'))
        ACCOUNT_EXECUTIVE=('account_execute', _('Account Execute'))
        TELLER=('teller', _('Teller'))
        BRANCH_MANAGER=('branch_manager',_('Branch Manager'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('username'), max_length=12, unique=True)
    security_question = models.CharField(
        _('Security Question'),
        max_length=50,
        choices=SecurityQuestion.choices
    )
    email = models.EmailField(_('Email Address'), unique=True, db_index=True)
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    ID_NUMBER = models.PositiveBigIntegerField(_('ID Number'), unique=True)
    account_status = models.CharField(
        _('Account Status'),
        max_length=50,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    role = models.CharField(
        _('Role'),
        max_length=50,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    failed_login_attempts = models.PositiveSmallIntegerField(null=True)
    last_failed_login_attempts = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True)
    otp_expiry_date = models.DateTimeField(_('OTP Expiry Date'), null=True, blank=True)
    security_answer=models.CharField(_('Security Answer'), max_length=50)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'ID_NUMBER',
        'security_question',
        'security_answer',
    ]

    def set_otp(self, otp:str)-> None:
        self.otp = otp
        self.otp_expiry_date = timezone.now() + settings.OTP_EXPIRATION
        self.save()

    def verify_otp(self, otp:str)-> bool:
        if self.otp == otp and self.otp_expiry_date > timezone.now():
            self.otp = ''
            self.otp_expiry_date = None
            self.save()
            return True
        else:
            return False

    def handle_failed_login_attempts(self):
        self.failed_login_attempts += 1
        self.last_failed_login_attempts = timezone.now()
        if self.failed_login_attempts >= settings.LOGIN_ATTEMPTS:
            self.account_status = self.AccountStatus.LOCKED
            self.save()
            send_account_locked_email(self)
        self.save()

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.last_failed_login_attempts = None
        self.account_status = self.AccountStatus.ACTIVE
        self.save()

    def unlock_account(self):
        if self.account_status == self.AccountStatus.LOCKED:
            self.account_status = self.AccountStatus.ACTIVE
            self.failed_login_attempts = 0
            self.last_failed_login_attempts = None
            self.save()

    @property
    def is_locked_out(self):
        if self.account_status == self.AccountStatus.LOCKED:
            if self.last_failed_login_attempts and (timezone.now() - self.last_failed_login_attempts) > settings.LOCKOUT_DURATION:
                self.unlock_account()
                return False
            return True
        return False

    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.title().strip()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-date_joined',)

    def has_role(self, role_name:str) -> bool:
        return hasattr(self, 'role') and self.role == role_name

    def __str__(self):
        return f'{self.full_name()} - {self.get_role_display()}'