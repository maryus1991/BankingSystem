from typing import Any

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction
from loguru import logger
from core_apps.common.permissions import IsAccountExecutive, IsTeller
from core_apps.common.renderers import GenricJSONRenderers


from .emails import send_account_creation_email, send_deposit_email
from .models import BankAccount
from .serializers import AccountVerificationSerializer, DepositSerializer, CustomerInfoSerializer



class AccountVerificationView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = AccountVerificationSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "verification"
    permission_classes = [IsAccountExecutive]

    def update(self, request:Request, *args:Any , **kwargs:Any)->Response:
        instance = self.get_object()

        if instance.kyc_verified and instance.fully_activated:
            return Response(
                {
                    "message": "This Account has already been verified and fully activated"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            kyc_submitted = serializer.validated_data.get(
                "kyc_submitted", instance.kyc_submitted
            )
            kyc_verified = serializer.validated_data.get(
                "kyc_verified", instance.kyc_verified
            )

            if kyc_verified and not kyc_verified:
                return Response(
                    {
                        "error": "KYC must be submitted before is can verified."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            instance.kyc_submitted = kyc_submitted
            instance.save()

            if kyc_verified and kyc_submitted:
                instance.kyc_verified = kyc_verified
                instance.verification_date = serializer.validated_data.get(
                    "verification_date", timezone.now()
                )
                instance.verification_notes = serializer.validated_data.get(
                    "verification_notes"
                )
                instance.verified_by = request.user
                instance.fully_activated = True
                instance.account_status = BankAccount.AccountStatus.ACTIVE
                instance.save()

                send_account_creation_email(
                    instance
                )
            return Response(
                {
                    "message": "Account Verification status updated successfully",
                    "data": self.get_serializer(instance)
                }
            )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "deposit"
    permission_classes = [IsTeller]


    def get(self, request: Request, *args:Any, **kwargs:Any)-> Response:
        account_number = request.query_params.get("account_number")

        if not account_number :
            return Response(
                {"error": "Account Number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = BankAccount.objects.get(
                account_number = account_number
            )
            serializer = CustomerInfoSerializer(account)
            return Response(serializer.data)
        except BankAccount.DoesNotExist:
            return Response(
                {"error": "Account Number is not exists"},
                status = status.HTTP_404_NOT_FOUND
            )

    @transaction.atomic()
    def create(self, request:Request, *args:Any, **kwargs:Any)->Response:
        serializer = self.get_serializer(date=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.context["account"]
        amount = serializer.validated_data["amount"]

        try:
            account.account_balance += amount
            account.full_clean()
            account.save()

            logger.info(f"Deposit of {amount} made to account {account.account_number} by teller {request.user.email}")

            send_deposit_email(
                account.user,
                account.user.email,
                account.currency,
                account.account_balance,
                account.account_number,
            )

            return Response(
                {
                    "message": f"Successfully deposit {amount} to account {account.account_number}"
                },
                status=status.HTTP_200_OK

            )

        except Exception as E:
            logger.error(f"Error during deposit: {str(e)}")
            return Response(
                {"error": "An error occurred during the deposit"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )