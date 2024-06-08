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
        extra_kwargs={
            "name":{"required":True},
            "link":{"required":True},
            "start_date":{"required":True},
            "description":{"required":True},
            "objectives":{"required":True},
            "tools":{"required":True},
        }
    
    def validate(self, attrs):
        end_date,ongoing=attrs.get("end_date"),attrs.get("ongoing")
        if end_date==None and ongoing==None:
            raise serializers.ValidationError("Either end date or ongoing should be set")

        if end_date:
            if ongoing: raise serializers.ValidationError("Can't set both end date and ongoing")
            start_date=attrs.get("start_date")
            if end_date<start_date:
                raise serializers.ValidationError("Start date should be before end date")

        return super().validate(attrs)