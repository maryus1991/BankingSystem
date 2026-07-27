from django.utils.translation import gettext_lazy as _
from rest_framework import  serializers
from decimal import Decimal
from .models import BankAccount


class CustomerInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.EmailField(source="user.email")


    class Meta :
        model = BankAccount
        fields = [
            "account_number",
            "full_name",
            "email",
            "account_balance",
            "account_type",
            "currency",
        ]


class DepositSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(1000.00)
    )

    class Meta:
        model= BankAccount
        fields = ["account_number", "amount"]

    def validate_account_number(self, value:str) -> str:
        try:
            account = BankAccount.objects.get(
                account_number = value
            )
            self.context["account"] = account
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError(_("Invalid account number"))

        return value

    def to_representation(self, instance: BankAccount) -> str :
        representation = super().to_representation(instance)
        representation["a"] = str(representation["amount"])
        return representation

class AccountVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = [
            "kyc_submitted",
            "kyc_verified",
            "verification_date",
            "verification_notes",
            "fully_activated",
            "account_status",
        ]
        read_only_fields = ["fully_activated"]

    def validate(self, data:dict)-> dict:
        kyv_verified = data.get("kyv_verified")
        verification_date = data.get("verification_date")
        verification_notes = data.get("verification_notes")

        if kyv_verified:
            if not verification_date:
                raise serializers.ValidationError(
                    _(
                        "Verification date is requires when verifying an account"
                    )
                )
            if not verification_notes:
                raise serializers.ValidationError(
                    _(
                        "Verification notes are requires when verifying an account"
                    )
                )
            if  kyv_verified and not all([
                kyv_verified, verification_date, verification_notes
            ]):
                raise serializers.ValidationError(
                    _(
                        "All Verification fields (Verification notes , date and kyc verified ) must be provided"
                    )
                )

        return data