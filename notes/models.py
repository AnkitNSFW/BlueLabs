from django.db import models

import sys
sys.path.append('')
from app.models import UserCred

class notes(models.Model):
    parent = models.ForeignKey(UserCred, on_delete=models.CASCADE)
    note_id = models.UUIDField()
    update_request_no = models.BigIntegerField(default = 0)
    title = models.CharField()
    note = models.CharField()

    pinned = models.BooleanField()
    shared = models.BooleanField(default=False)

    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()