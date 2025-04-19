"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

from core_apps.user_auth.views import TestLoggingView

import os

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # path("", TestLoggingView.as_view(), name="home"),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger/', SpectacularSwaggerView.as_view(), name='schema-swagger'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(), name='schema-redoc'),
]

admin.site.site_header = str(os.getenv('BANK_NAME')) + 'Admin'
admin.site.site_title = str(os.getenv('BANK_NAME')) + 'Admin Portal '
admin.site.index_title = 'Welcome to ' + str(os.getenv('BANK_NAME')) + 'Admin Portal'