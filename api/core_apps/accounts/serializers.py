from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import  serializers
from decimal import Decimal
from .models import BankAccount, Transaction
from ..user_auth.models import User


class UUIDField(serializers.Field):
    def to_representation(self, value) -> str:
        return str(value)

class TransactionSerializer(serializers.ModelSerializer):
    id = UUIDField(read_only=True)
    sender_account = serializers.CharField(max_length=20, required=False)
    receiver_account = serializers.CharField(max_length=20, required=False)

    amount = serializers.DecimalField(
        max_digits=100000, decimal_places=2, min_value=1000.00,
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "description",
            "status",
            "transaction_type",
            "created_at",
            "sender",
            "receiver",
            "sender_account",
            "receiver_account",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def to_representation(self, instance:Transaction) -> dict[str, Any]:
        representation = super().to_representation(instance)
        representation["amount"] = str(representation["amount"])
        representation["sender"] = str(instance.sender.full_name if instance.sender else None )
        representation["receiver"] = str(instance.receiver.full_name if instance.receiver else None )
        representation["sender_account"] = str(instance.sender_account.account_number if instance.sender_account else None )
        representation["receiver_account"] = str(instance.receiver_account.account_number if instance.receiver_account else None )

        return representation

    def validate(self, data):
        transaction_type = data.get("transaction_type")
        sender_account_number = data.get("sender_account")
        receiver_account_number = data.get("receiver_account")

        amount = data.get("amount")

        try:
            if transaction_type == Transaction.TransactionType.WITHDRAWAL:
                account = BankAccount.objects.get(account_number=sender_account_number)
                data["sender_account"] = account
                data["receiver_account"] = None

                if account.account_balance < amount:
                    raise serializers.ValidationError(
                        "Insufficient found for withdrawal"
                    )
            elif transaction_type == Transaction.TransactionType.DEPOSIT:
                account = BankAccount.objects.get(
                    account_number = receiver_account_number
                )
                data["sender_account"] = None
                data["receiver_account"] = account
            else:
                sender_account = BankAccount.objects.get(
                    account_number = sender_account_number
                )
                receiver_account = BankAccount.objects.get(
                    account_number = receiver_account_number
                )

                data["sender_account"] = sender_account
                data["receiver_account"] = receiver_account

                if sender_account == receiver_account:
                    raise serializers.ValidationError(
                        "Sender and receiver accounts must be different"
                    )
                if sender_account.currency != receiver_account.currency:
                    raise serializers.ValidationError(
                        "Transfer are only allowed between account with the same currency"
                    )

                if sender_account.account_balance < amount:
                    raise serializers.ValidationError(
                        "Insufficient found for transfer"
                    )
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError(
                "One of both account are not fount"
            )

        return data


class SecurityQuestionSerializer(serializers.Serializer):
    security_answer = serializers.CharField(max_length=100)

    def validate(self, data:dict)-> dict:
        user = self.context["request"].user
        if data["security_answer"] != user.security_answer:
            raise serializers.ValidationError("Incorrect security answer")

        return data

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate(self, data:dict)-> dict:
        user = self.context["request"].user
        if not user.verify_otp(data["otp"]):
            raise serializers.ValidationError("Invalid or Expired OTP")

        return data

class UsernameVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)

    def validate_username(self, value:dict)-> dict:
        user = self.context["request"].user
        if user.username != value:
            raise serializers.ValidationError("Invalid Username")

        return value



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