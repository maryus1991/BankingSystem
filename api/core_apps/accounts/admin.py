from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import BankAccount, Transaction

User = get_user_model()


admin.site.register(Transaction)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
     list_display = [
         "account_number",
         "user",
         "currency",
         "account_type",
         "account_balance",
         "account_status",
         "is_primary",
         "kyc_verified",
         "get_verified_by",
     ]

     list_filter = [

         "currency",
         "account_type",
         "account_balance",
         "account_status",
         "is_primary",
         "kyc_verified",
         "kyc_submitted",
      ]

     search_fields = [
         "account_number",
         "user__email",
         "user__first_name",
         "user__last_name",
     ]

     readonly_fields = [
         "account_number",
         "created_at",
         "updated_at",
     ]

     def get_verified_by(self, obj):
         return obj.verified_by.full_name if obj.verified_by else "-"


     get_verified_by.short_description = _("Verified BY")
     get_verified_by.admin_order_field = "verified_by__first_name"

     def get_queryset(self, request):
         query = super().get_queryset(request)
         if request.user.is_superuser:
             return query

         return query.filter(verified_by = request.user)

     def has_change_permission(self, request, obj = ...):
         if not obj:
             return True

         return request.user.is_superuser or obj.verified_by == request.user

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
         if db_field.name == "verified_by":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        
         return super().formfield_for_foreignkey(db_field, request, **kwargs)