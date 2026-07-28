from django.urls import path
from .views import (
    AccountVerificationView,
    DepositView,
    InitiateWithdrawalView,
    VerifyUsernameAndWithdrawAPIView
)


app_name = "accounts"


urlpatterns = [
    path("verify/<uuid:pk>/", AccountVerificationView.as_view(), name="verification"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("initiate-withdrawal/", InitiateWithdrawalView.as_view(), name="initiate-withdrawal"),
    path("verify-username-and-withdrawal/", VerifyUsernameAndWithdrawAPIView.as_view(), name="verify-username-and-withdrawal"),
]