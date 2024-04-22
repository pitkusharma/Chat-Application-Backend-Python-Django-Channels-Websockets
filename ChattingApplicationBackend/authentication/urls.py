from django.urls import path
from .views import Login, RefreshToken, VerifyAccessToken


urlpatterns = [
    path('login/', Login.as_view()),
    path('refresh/', RefreshToken.as_view()),
    path('verify/', VerifyAccessToken.as_view()),
]