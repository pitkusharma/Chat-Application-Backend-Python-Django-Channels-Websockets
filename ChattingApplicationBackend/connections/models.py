from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

Users = get_user_model()

class Connections(models.Model):
    status = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sent_by = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='sent_by')
    sent_to = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='sent_to')
    status = models.CharField(max_length=10, choices=status, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    status_updated_at = models.DateTimeField(null=True, blank=True)
