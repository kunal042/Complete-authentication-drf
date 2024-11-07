from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mainapp import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/<int:pk>/', views.UserSignupView.as_view(), name='user-detail'),
    path('login/', views.LoginView.as_view(), name='login-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)