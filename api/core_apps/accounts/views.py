from random import randint
from typing import Any

from django.utils import timezone
from phonenumbers.geocoder import description_for_number
from rest_framework import generics, status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction

from decimal import  Decimal
from loguru import logger
from core_apps.common.permissions import IsAccountExecutive, IsTeller
from core_apps.common.renderers import GenricJSONRenderers


from .models import BankAccount, Transaction
from .serializers import (
    AccountVerificationSerializer,
    DepositSerializer,
    CustomerInfoSerializer,
    TransactionSerializer,
    UsernameVerificationSerializer,
    SecurityQuestionSerializer,
    OTPVerificationSerializer,

)
from .emails import (
    send_account_creation_email,
    send_deposit_email,
    send_transfer_email,
    send_withdrawal_email,
    send_transfer_otp_email
)


class VerifiedOTPView(generics.CreateAPIView):
    serializer_class = OTPVerificationSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "verify_otp"

    def create(self, request:Request, *args:Any, **kwargs:Any):
        serializer = self.get_serializer(
            data= request.data, context = {"request": request}
        )

        if serializer.is_valid():
            return self.process_transfer(request)

        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )

    def process_transfer(self, request:Request)-> Response:
        transfer_data = request.session.get("transfer_data")

        if not transfer_data:
            return Response(
                    {
                        "error": "Transfer Data not fount, Please start the process again"
                    }
                    ,status=status.HTTP_403_FORBIDDEN
                )

        try:
            sender_account = BankAccount.objects.get(account_number = transfer_data["sender_account"])
            receiver_account = BankAccount.objects.get(account_number = transfer_data["receiver_account"])

        except BankAccount.DoesNotExist:
            return Response(
                    {
                        "error": "One or both accounts not found"
                    }
                    ,status=status.HTTP_404_NOT_FOUND
                )

        amount = Decimal(transfer_data)

        if sender_account.account_balance < amount:
            return Response(
                    {
                        "error": "Insufficient funds for transfer"
                    }
                    ,status=status.HTTP_400_BAD_REQUEST
                )

        sender_account.account_balance -= amount
        receiver_account += amount
        sender_account.save()
        receiver_account.save()

        transfer_transaction = Transaction.objects.create(
            user=request.user,
            sender = request.user,
            sender_account = sender_account,
            receiver = receiver_account.user,
            receiver_account = receiver_account,
            amount=amount,
            description=transfer_data.get("description", ""),
            transaction_type=Transaction.TransactionType.TRANSFER,
            transaction_statua=Transaction.TransactionStatus.COMPLETED
        )

        del request.session["transfer_data"]

        send_transfer_email(
            sender_email = sender_account.user.email,
            receiver_email= receiver_account.user.email,
            sender_name=sender_account.user.full_name,
            receiver_name=receiver_account.user.full_name,
            amount=amount,
            currency=sender_account.currency,
            sender_new_balance=sender_account.account_balance,
            receiver_new_balance=receiver_account.account_balance,
            sender_account_number=sender_account.account_number,
            receiver_account_number=receiver_account.account_number,
        )

        logger.info(
            "Transfer of {} {} made from account {} to {} ".format(
                amount,
                sender_account.currency,
                sender_account.account_number,
                receiver_account.account_number)
        )

        return Response(
            TransactionSerializer(transfer_transaction).data,
            status=status.HTTP_200_OK
        )

class VerifySecurityQuestionView(generics.CreateAPIView):
    serializer_class = SecurityQuestionSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "verification_answer"

    def create(self, request:Response, *args:Any, **kwargs:Any)->Response:
        serializer = self.get_serializer(
            data= request.data, context = {"request": request}
        )

        if serializer.is_valid():
            otp = "".join([str(randint(0,9)) for _ in range(6)])
            request.user.set_otp(otp)
            send_transfer_otp_email(request.user.email, otp)
            return Response({
                "message":  "Security question verified, An OTP has been sent to your email ",
                "next_step":  "verify_otp",
            },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )

class InitiateTransferView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "initiate_transfer"

    def create(self, request:Response, *args:Any, **kwargs:Any)->Response:
        data = request.data.copy()
        data["transaction_type"] = Transaction.TransactionType.TRANSFER

        sender_account_number = data.get("sender_account")
        receiver_account_number = data.get("receiver_account")

        try:
            sender_account = BankAccount.objects.get(account_number=sender_account_number, user=request.user )

            if not (sender_account.fully_activated and sender_account.kyc_verified):
                return Response(
                    {
                        "error": "This is not fully verified, Please completed the verification process by visiting any of our local bank branches"
                    }
                    ,status=status.HTTP_403_FORBIDDEN
                )
        except BankAccount.DoesNotExist:
            return Response(
                {
                    "error": "sender account number found or you're not authorized to use this account "
                }
                , status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            request.session["transfer_data"] = {
                "sender_account": sender_account_number,
                "receiver_account": receiver_account_number,
                "amount": str(serializer.validated_data["data"]),
                "descriptor": serializer.validated_data.get("description", ""),
            }
            return Response(
                {
                    "message": "Please answer your security question to proceed with the transfer",
                    "next_step": "verify_security_question"
                },
                status=status.HTTP_200_OK
            )

        return  Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class InitiateWithdrawalView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "initiate_withdrawal"

    def create(self, request:Request, *args:Any, **kwargs:Any)-> Response:
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")

        if not account_number:
            return Response(
                {"error": "Account number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = BankAccount.objects.get(
                account_number = account_number,
                user= request.user
            )

            if not (account.fully_activated and account.kyc_verified):
                return Response(
                    {"error": "Your Account is not fully verified please complete verification process "},
                    status=status.HTTP_403_FORBIDDEN
                )
        except BankAccount.DoesNotExist:
            return Response(
                {
                    "error": "Your are not authorize to withdrawal from this account "
                }
                ,status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            data = {
                "amount": amount,
                "description": "Withdrawal from account {}".format(account_number),
                "transaction_type": Transaction.TransactionType.WITHDRAWAL,
                "sender_account": account_number,
                "receiver_account":account_number
            }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = serializer.validated_data.get("amount")

        if account.account_balance < amount:
            return Response(
                {
                    "error": "Insufficient funds for withdrawal "
                },status=status.HTTP_400_BAD_REQUEST
            )

        request.session["withdrawal_data"] = {
            "account_number": account_number,
            "amount":str(amount)
        }
        logger.info("Withdrawal data stored in session")

        return Response(
            {
                "message": "Withdrawal Initiate, Please verify, your username to complete the withdrawal ",
                "next_step": "Verify your username to complete the withdrawal"
            },
            status=status.HTTP_200_OK
        )

class VerifyUsernameAndWithdrawAPIView(generics.CreateAPIView):
    serializer_class = UsernameVerificationSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "verify_username_and_withdrawal"

    @transaction.atomic
    def create(self, request:Request, *args:Any, **kwargs:Any)-> Response:
        serializer = self.get_serializer(
            data= request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        withdrawal_data = request.session.get("withdrawal_data")

        if not withdrawal_data:
            return Response(
                {"error": "No pending withdrawal found, please initiate a withdrawal first"}
                ,status=status.HTTP_400_BAD_REQUEST
            )

        account_number = withdrawal_data["account_number"]
        amount = Decimal(withdrawal_data["amount"])

        try:
            account = BankAccount.objects.get(
                account_number=account_number, user=request.user
            )
        except BankAccount.DoesNotExist:
            return Response(
                {
                    "error":"Account Number does not Exist"
                }
                ,status=status.HTTP_404_NOT_FOUND
            )

        if account.account_balance < amount:
            return Response(
                {
                    "error": "Insufficient funds for withdrawal "
                },status=status.HTTP_400_BAD_REQUEST
            )

        account.account_balance -= amount
        account.save()

        withdrawal_transaction = Transaction.objects.create(
            user = request.user,
            sender = request.user,
            sender_account = account,
            amount=amount,
            description=f"withdrawal from account {account_number}",
            transaction_type = Transaction.TransactionType.WITHDRAWAL,
            status=Transaction.TransactionStatus.COMPLETED
        )
        logger.info("Withdrawal of {} made from {}".format(amount, account_number))

        send_withdrawal_email(
            user=account.user,
            user_email=account.user.email,
            amount=amount,
            currency=account.currency,
            new_balance=account.account_balance,
            account_number=account.account_number
        )

        del request.session["withdrawal_data"]
        return Response({
            "message": "Withdrawal completed successfully",
            "transaction": TransactionSerializer(withdrawal_transaction).data,
        },
        status=status.HTTP_200_OK
        )

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
            logger.error(f"Error during deposit: {str(E)}")
            return Response(
                {"error": "An error occurred during the deposit"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )