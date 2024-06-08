from .models import Experience
from rest_framework import serializers

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Experience
        fields=[
            "id","company","title","user","link","display","start_date",
            "end_date","ongoing","description","objectives","tools"
        ]
        read_only_fields=["user"]
        extra_kwargs={
            "company":{"required":True},
            "title":{"required":True},
            "link":{"required":True},
            "display":{"required":True},
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