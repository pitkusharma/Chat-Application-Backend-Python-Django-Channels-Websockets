from django.db import models
from django.contrib.auth import get_user_model


Users = get_user_model()

class LoginData(models.Model):
    user = models.ForeignKey(Users, on_delete=models.RESTRICT)
    username = models.CharField(max_length=20)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
