from django.utils.translation import gettext_lazy as _
from rest_framework import  serializers
from .models import BankAccount



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