from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user=models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )
    bio=models.TextField(null=True,blank=True)
    skills=models.JSONField(null=True,blank=True)
    socials=models.JSONField(null=True,blank=True)

    def __str__(self):
        return "%s %s" %(self.user.first_name,self.user.last_name)