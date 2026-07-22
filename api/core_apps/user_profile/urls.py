from django.urls import path

from .views import (
    NextOfKinDetailAPIView,
    NextOfKinAPIView,
    ProfileListAPIView,
    ProfileDetailAPIView
)

app_name = "profile"


urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="profile-list"),
    path("my-profile/", ProfileListAPIView.as_view(), name="profile-detail"),
    path("my-profile/next-of-kin/", NextOfKinAPIView.as_view(), name="next-of-kin-list"),
    path("my-profile/next-of-kin/<uuid:pk>", NextOfKinDetailAPIView.as_view(), name="next-of-kin-detail"),
]