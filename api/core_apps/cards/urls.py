from django.urls import path


from .views import (
    VirtualCardListCreateAPIView,
    VirtualCardDetailAPIView,
    VirtualCardTopUpAPIView,
)


app_name = "cards"

urlpatterns = [
    path("virtual-card/", VirtualCardListCreateAPIView.as_view(), name="list-create"),
    path("virtual-card/<uuid:pk>", VirtualCardDetailAPIView.as_view(), name="detail"),
    path("virtual-card/<uuid:pk>/top-up", VirtualCardTopUpAPIView.as_view(), name="top-up"),
]