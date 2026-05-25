from rest_framework import serializers
from .models import NormalizedRecord


class NormalizedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalizedRecord
        fields = "__all__"