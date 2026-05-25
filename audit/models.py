from django.db import models
from normalization.models import NormalizedRecord


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("CREATED", "Created"),
        ("UPDATED", "Updated"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    record = models.ForeignKey(NormalizedRecord, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    changed_by = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} - {self.record.id}"