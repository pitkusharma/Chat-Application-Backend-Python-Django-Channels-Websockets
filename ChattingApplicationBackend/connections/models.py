from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()

class Connections(models.Model):
    status = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    )
    connection_sent_by = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='connection_sent_by')
    connection_sent_to = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='connection_sent_to')
    request_status = models.CharField(max_length=10, choices=status, default='pending')
    connection_sent_at = models.DateTimeField(auto_now_add=True)
    status_updated_at = models.DateTimeField(null=True, blank=True)
