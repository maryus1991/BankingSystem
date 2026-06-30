 
from django.contrib import admin
from django.urls import path

from django.conf import settings

print(settings.ADMIN_URL)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]
