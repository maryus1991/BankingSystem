from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    name = 'core_apps.accounts'
    verbose_name = _("Account")