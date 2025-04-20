from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('email','username' ,'first_name', 'last_name'
                    ,'is_staff', 'role', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'role', 'email')

    fieldsets = (
        (
            _("Auth Credentials"),
            {'fields': (
                'username',
                'email',
                'password'
                ),
            },
        ),
        (
            _("Personal Information"),
            {'fields': (
                'first_name',
                'last_name',
                'ID_NUMBER',
                'role',
            ),}
        ),(
           _('Account Status'),
           {
               "fields": (
                   'account_status',
                   'failed_login_attempts',
                   'last_failed_login_attempts',
               ),
           },
        ),(
            _('Security'),{
                'fields': (
                    'security_question',
                    'security_answer',
                ),
            },
        ),(
            _('Permissions'),{
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'is_active',
                    "user_permissions",
                ),
            },
        ),(
            _('Dates'),{
                'fields': (
                    'last_login',
                    'date_joined',

                ),
            },
        ),
    )
    search_fields = ('email','first_name','last_name','username', 'ID_NUMBER')
    ordering = ('email','first_name','last_name','username')