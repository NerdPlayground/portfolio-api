from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True,allow_blank=False)
    password=serializers.CharField(style={'input_type': 'password'})

class ContactUserSerializer(serializers.Serializer):
    name=serializers.CharField(required=True,allow_blank=False)
    sender=serializers.EmailField(required=True,allow_blank=False)
    receiver=serializers.EmailField(required=True,allow_blank=False)
    message=serializers.CharField(required=True,allow_blank=False)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['bio','skills','socials']

class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()

    class Meta:
        model=get_user_model()
        fields=['username','first_name','last_name','email','profile']
    
    def update(self,instance,validated_data):
        profile=Profile.objects.get(user=instance)
        profile_data=validated_data.pop("profile")
        profile.bio=profile_data["bio"]
        profile.skills=profile_data["skills"]
        profile.socials=profile_data["socials"]
        profile.save()

        instance.username=validated_data["username"]
        instance.first_name=validated_data["first_name"]
        instance.last_name=validated_data["last_name"]
        instance.email=validated_data["email"]
        instance.save()

        return instance