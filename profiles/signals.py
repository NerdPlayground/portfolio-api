from .models import Profile
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender,instance,created,**kwargs):
    if not created: return
    profile=Profile.objects.create(user=instance)
    profile.save()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    recipient="{} {}".format(reset_password_token.user.first_name,reset_password_token.user.last_name)
    email_plaintext_message="Open the link to reset your password:\nLink: {}\nAuthentication Token: {}".format(
        instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        reset_password_token.key
    )
    send_mail(
        "Password Reset for {}".format(recipient), # title
        email_plaintext_message, # message
        "info@yourcompany.com", # sender
        [reset_password_token.user.email], # receiver
        fail_silently=False,
    )