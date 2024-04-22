from django.urls import path
from .views import CreateConnection


urlpatterns = [
    path('create-connection/', CreateConnection.as_view()),
]