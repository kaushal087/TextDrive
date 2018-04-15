import uuid
from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4,
                          db_index=True, help_text='Defines the id.')

    user = models.OneToOneField(User, related_name='folder',
                             on_delete=models.CASCADE, unique=True)

    folder_id = models.CharField(max_length=255, null=True, blank=True,
                                 help_text='Defines the folder id of user')

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False,
                                      help_text='creation time')

    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,
                                      help_text='updation time')

    class Meta:
        db_table = 'folders'
        verbose_name = 'drive directories'
        get_latest_by = 'created_at'
