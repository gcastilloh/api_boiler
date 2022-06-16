from rest_framework import serializers
from .models import Programs, CurrentProgram

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = "__all__"
        read_only = (
            "id",
        )


class CurrentProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentProgram
        fields = "__all__"
        read_only = (
            "id",
        )