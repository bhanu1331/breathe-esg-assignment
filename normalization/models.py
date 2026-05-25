from django.db import models
from tenants.models import Tenant
from ingestion.models import RawRecord

class NormalizedRecord(models.Model):
    SCOPE_CHOICES = [
        ("SCOPE_1", "Scope 1"),
        ("SCOPE_2", "Scope 2"),
        ("SCOPE_3", "Scope 3"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    raw_record = models.ForeignKey(RawRecord, on_delete=models.CASCADE)

    activity_type = models.CharField(max_length=100)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)

    original_value = models.FloatField()
    original_unit = models.CharField(max_length=50)

    normalized_value = models.FloatField()
    normalized_unit = models.CharField(max_length=50)

    suspicious = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("APPROVED", "Approved"),
            ("REJECTED", "Rejected"),
            ("LOCKED", "Locked"),
            ("FAILED", "Failed"),
        ],
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.scope}"