from .models import Project
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=[
            "id","name","user","link","start_date","end_date",
            "ongoing","description","objectives","tools"
        ]
        read_only_fields=["user"]