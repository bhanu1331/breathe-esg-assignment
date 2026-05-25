from django.db import models
from tenants.models import Tenant


class DataSource(models.Model):
    SOURCE_TYPES = [
        ("SAP", "SAP"),
        ("UTILITY", "Utility"),
        ("TRAVEL", "Travel"),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tenant.name} - {self.source_type}"


class RawRecord(models.Model):
    VALIDATION_STATUS = [
        ("VALID", "Valid"),
        ("INVALID", "Invalid"),
    ]

    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    raw_payload = models.JSONField()
    validation_status = models.CharField(max_length=20, choices=VALIDATION_STATUS)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Raw Record {self.id}"