from django.db import models
from pocket.models import Achievement
from django.contrib.auth import get_user_model

class Experience(Achievement):
    user=models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    company=models.CharField(max_length=100,null=True,blank=True)
    title=models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        ordering=["start_date"]

    def __str__(self):
        return self.title