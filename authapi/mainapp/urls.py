
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name="register"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('userlist/', views.UserListView.as_view(), name="userlist"),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('ChangePassword/', views.UserChangePasswordView.as_view(), name="ChangePassword"),
    path('email-send/', views.UserChangePasswordView.as_view(), name="email-send"),
    path('rest-email-view/', views.UserPasswordResetView.as_view(), name="rest-email-view"),
]