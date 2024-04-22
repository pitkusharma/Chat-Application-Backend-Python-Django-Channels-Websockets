from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


Users = get_user_model()


class PersonalMessages(models.Model):
    message_sent_by = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='message_sent_by')
    message_sent_to = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='message_sent_to')
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class UserGroups(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    group_name = models.CharField(max_length=20)
    group_created_by = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='groups_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupMembers(models.Model):
    group = models.ForeignKey(UserGroups, on_delete=models.RESTRICT, related_name='group_members')
    user = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='user_groups')
    added_by = models.ForeignKey(Users, on_delete=models.RESTRICT, related_name='user_adds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




