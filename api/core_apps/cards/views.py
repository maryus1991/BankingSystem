from decimal import  Decimal, InvalidOperation
from typing import Any

from loguru import logger

from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.request import Request

from core_apps.accounts.models import Transaction
from core_apps.common.renderers import GenricJSONRenderers

from .emails import send_virtual_card_topup_email
from .models import VirtualCard
from .serializers import VirtualCardSerializer, VirtualCardCreateSerializer


class VirtualCardListCreateAPIView(generics.ListCreateAPIView):
    renderer_classes = [GenricJSONRenderers]
    object_label = "visa_card"

    def get_queryset(self):
        return VirtualCard.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return VirtualCardCreateSerializer
        return VirtualCardSerializer

    def create(self, request:Request, *args:any, **kwargs:Any)->Response:
        if request.user.virtual_cards.count() >= 3:
            return Response(
                {
                    "error": "You can only have up to 3 virtual cards at one time "
                },status= status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_account_number = serializer.validated_data.get("bank_account_number")
        user_bank_accounts = request.user.bank_accounts.all()

        if not user_bank_accounts.filter(account_number=bank_account_number).exists():
            return Response(
                {
                    "error": "You can only create virtual bank account link to you  own bank account"
                },status= status.HTTP_403_FORBIDDEN
            )

        virtual_card = serializer.save()
        logger.info(f"Visa card umber {virtual_card.card_number} create for user {request.user.email}")

        return Response(
            VirtualCardSerializer(virtual_card).data,
            status=status.HTTP_201_CREATED
        )


class VirtualCardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VirtualCardSerializer
    renderer_classes = [GenricJSONRenderers]
    object_label = "visa_card"

    def get_queryset(self):
        return VirtualCard.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You can not perform this action, because the card is not belong to you.")

        return obj

    def destroy(self, request:Request, *args:Any, **kwargs:Any)-> Response:
        try:
            instance = self.get_object()
            if instance.balance >= 0:
                return Response(
                    {"error": "Can not delete a card with non-zero balance  "},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.warning(
                "Visa card number {}, belonging to {} destroyed, Request-User: {}".format(instance.card_number, instance.user.full_name, request.user),
            )
            self.perform_destroy(instance)
            return Response(
                {"message": "Card successfully deleted"},
                status=status.HTTP_200_OK
            )
        except VirtualCard.DoesNotExist:
            return Response(
                {"error": "Card Not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except PermissionDenied as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        except Exception as e:
            logger.error("Error deleting card:{}".format(e))
            return Response(
                {"error": "An unexpected error occurred while deleting the card"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VirtualCardTopUpAPIView(generics.UpdateAPIView):
    renderer_classes = [GenricJSONRenderers]
    object_label = "visa_card"

    def get_queryset(self):
        return VirtualCard.objects.filter(user=self.request.user)

    @transaction.atomic
    def update(self, request:Request, *args:Any, **kwargs:Any)->Response:
        virtual_card = self.get_object()
        amount = request.data.get("amount")

        if not amount:
            return Response(
                {"error": "Amount must be provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return Response(
                {"error": f"The amount {amount} is not valid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than zero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bank_account = virtual_card.bank_account

        if bank_account.account_balance < amount:
            return Response(
                {"error": "Insufficient founds is the bank account"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bank_account.account_balance -= amount
        virtual_card.balance += amount

        bank_account.save()
        virtual_card.save()

        transaction = Transaction.objects.create(
            user = request.user,
            amount=amount,
            description="Top-p for visa card ending in {}".format(virtual_card.card_number[-4:]),
            transaction_type = Transaction.TransactionType.DEPOSIT,
            status = Transaction.TransactionStatus.COMPLETED,
            sender = request.user,
            receiver = request.user,
            sender_account = bank_account,
            receiver_account = bank_account,
        )
        send_virtual_card_topup_email(
            request.user,
            virtual_card,
            amount,
            virtual_card.balance,
        )
        logger.info(
            f"Visa card {virtual_card.card_number} has been top up with {amount} by {virtual_card.user.full_name}, Transaction ID: {transaction.id} "
        )

        return Response(VirtualCardSerializer(virtual_card).data)

