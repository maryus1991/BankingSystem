from django.urls import path

from .views import AccountVerificationView, DepositView


app_name = "accounts"


urlpatterns = [
    path("verify/<uuid:pk>/", AccountVerificationView.as_view(), name="account-verification"),
    path("deposit/", DepositView.as_view(), name="account-deposit"),
]