"""
URL configuration for errandsmate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Temporarily commented out JWT imports
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import home
from errands.urls import api_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # Temporarily commented out JWT URLs
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include((api_urlpatterns, 'api'))),  # API URLs with 'api' namespace
    path('errands/', include('errands.urls', namespace='errands')),  # Template URLs with 'errands' namespace
    path('notifications/', include('notifications.urls', namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
