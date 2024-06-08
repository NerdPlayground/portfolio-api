import uuid
from django.db import models

class Achievement(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    display=models.BooleanField(default=False,blank=True)
    link=models.URLField(null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    ongoing=models.BooleanField(default=False,blank=True)
    description=models.TextField(null=True,blank=True)
    objectives=models.JSONField(null=True,blank=True)
    tools=models.JSONField(null=True,blank=True)

    class Meta:
        abstract=True