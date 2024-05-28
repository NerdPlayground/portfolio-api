from .models import Experience
from rest_framework import serializers

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Experience
        fields=[
            "id","company","title","user","link","start_date",
            "end_date","ongoing","description","objectives","tools"
        ]
        read_only_fields=["user"]