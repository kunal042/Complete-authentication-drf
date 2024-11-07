"""
URL configuration for oddless project.

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
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('api.urls')),
# ]

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from api import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creating Router Object
# router = DefaultRouter()

# router.register("user", views.UserSignupView, basename='user')

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),
    path('signup/', views.UserView.as_view()),
    path('signup/<int:pk>/', views.UserSignupView.as_view()),

     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)