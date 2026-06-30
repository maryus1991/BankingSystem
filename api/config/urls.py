 
from django.contrib import admin
from django.urls import path
from django.conf import settings

from core_apps.user_profile.views import Test

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", Test.as_view(), name="homa")
]
