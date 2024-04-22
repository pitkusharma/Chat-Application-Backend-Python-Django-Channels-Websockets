from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_online = models.BooleanField(default=False)
    # about = models.CharField(max_length=200, null=True, blank=True)
    # profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

