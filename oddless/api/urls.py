# from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static
# from rest_framework import routers

# from api import views

# router = routers.SimpleRouter()
# router.register(r'users', views.Userview, basename='user')

# urlpatterns = [
#     # Other URL patterns
# #    path('', views.UserSignupView.as_view()),
# #    path('', views.Userview.as_view()),
#    path('', include('router.urls')),


# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)