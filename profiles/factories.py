import factory
import factory.fuzzy
from .models import Profile
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=get_user_model()
    
    username=factory.LazyAttribute(lambda e: "{}{}".format(e.first_name,e.last_name).lower())
    first_name=factory.Faker("first_name")
    last_name=factory.Faker("last_name")
    email=factory.LazyAttribute(lambda e: "{}@gmail.com".format(e.username).lower())
    password=factory.django.Password("qwerty123!@#")

class ProfilesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Profile
    
    user=factory.SubFactory(UserFactory)
    bio=factory.Faker("paragraph",nb_sentences=5)
    skills=factory.List(["Python","Django","Django REST Framework"])
    socials=factory.Dict({
        "twitter": "https://x.com",
        "github": "https://github.com",
        "instagram": "https://instagram.com",
    })