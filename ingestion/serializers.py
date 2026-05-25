from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField()
    uploaded_by = serializers.CharField(max_length=255)
    file = serializers.FileField()