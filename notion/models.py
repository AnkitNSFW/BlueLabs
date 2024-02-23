from django.db import models

import sys
sys.path.append('')
from app.models import UserCred

# Create your models here.
class NotionWidgets(models.Model):
    parent = models.ForeignKey(UserCred, on_delete=models.CASCADE)
    
    user_id = models.EmailField()
    widget_id = models.UUIDField()
    name = models.CharField()
    widget_name = models.CharField()
    widget_config = models.JSONField()

    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

class WidgetsTracker(models.Model):
    parent = models.OneToOneField(UserCred, on_delete=models.CASCADE)
    widget_count = models.JSONField()
    modified_at = models.DateTimeField()