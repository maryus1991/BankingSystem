from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'ID_NUMBER', 'first_name', 'last_name', 'security_question',
                  'security_answer', 'is_staff', 'is_superuser')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'))
        return email

    def clean_ID_NUMBER(self):
        ID_NUMBER = self.cleaned_data.get('ID_NUMBER')
        if User.objects.filter(ID_NUMBER=ID_NUMBER).exists():
            raise ValidationError(_('This ID number is already in use.'))
        return ID_NUMBER

    def clean(self):
        clean_data = super().clean()
        is_superuser = clean_data.get('is_superuser')
        security_question = clean_data.get('security_question')
        security_answer = clean_data.get('security_answer')

        if not is_superuser :
            if not security_question:
                self.add_error('security_question', _('Security question is required.'))

            if not security_answer:
                self.add_error('security_answer', _('Security answer is required.'))

        return clean_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        return user

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'ID_NUMBER', 'first_name', 'last_name', 'security_question',
                  'security_answer', 'is_staff', 'is_superuser')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'))
        return email

    def clean_ID_NUMBER(self):
        ID_NUMBER = self.cleaned_data.get('ID_NUMBER')
        if User.objects.exclude(pk=self.instance.pk).filter(ID_NUMBER=ID_NUMBER).exists():
            raise ValidationError(_('This ID number is already in use.'))
        return ID_NUMBER