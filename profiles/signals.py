from .models import Profile
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender,instance,created,**kwargs):
    if not created: return
    profile=Profile.objects.create(user=instance)
    profile.save()