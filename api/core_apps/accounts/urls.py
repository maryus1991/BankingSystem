from django.urls import path

from .views import AccountVerificationView


app_name = "accounts"


urlpatterns = [
    path("verify/<uuid:pk>/", AccountVerificationView.as_view(), name="account-verification")
]