from django.urls import path
from .views import (
    AccountVerificationView,
    DepositView,
    InitiateWithdrawalView,
    VerifyUsernameAndWithdrawAPIView,
    InitiateTransferView,
    VerifiedOTPView,
    VerifySecurityQuestionView,
    TransactionListAPIView,
    TransactionPDFView
)


app_name = "accounts"


urlpatterns = [
    path("verify/<uuid:pk>/", AccountVerificationView.as_view(), name="verification"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("initiate-withdrawal/", InitiateWithdrawalView.as_view(), name="initiate-withdrawal"),
    path("verify-username-and-withdrawal/", VerifyUsernameAndWithdrawAPIView.as_view(), name="verify-username-and-withdrawal"),

    path("transfer/initiate/", InitiateTransferView.as_view(), name="transfer-initiate"),
    path("transfer/verify/security-question/", VerifySecurityQuestionView.as_view(), name="transfer-verify-security-question"),
    path("transfer/verify/otp/", VerifiedOTPView.as_view(), name="transfer-verify-otp"),

    path("transactions/", TransactionListAPIView.as_view(), name="transaction-list"),
    path("transactions/pdf/", TransactionPDFView.as_view(), name="transaction-pdf"),
]