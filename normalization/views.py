from rest_framework.views import APIView
from rest_framework.response import Response

from .models import NormalizedRecord
from .serializers import NormalizedRecordSerializer
from audit.models import AuditLog


class RecordListView(APIView):
    def get(self, request):
        records = NormalizedRecord.objects.all().order_by("-created_at")
        serializer = NormalizedRecordSerializer(records, many=True)
        return Response(serializer.data)


class SuspiciousRecordView(APIView):
    def get(self, request):
        records = NormalizedRecord.objects.filter(suspicious=True)
        serializer = NormalizedRecordSerializer(records, many=True)
        return Response(serializer.data)


class PendingRecordView(APIView):
    def get(self, request):
        records = NormalizedRecord.objects.filter(status="PENDING")
        serializer = NormalizedRecordSerializer(records, many=True)
        return Response(serializer.data)


class FailedRecordView(APIView):
    def get(self, request):
        records = NormalizedRecord.objects.filter(status="FAILED")
        serializer = NormalizedRecordSerializer(records, many=True)
        return Response(serializer.data)


class ApproveRecordView(APIView):
    def patch(self, request, record_id):
        record = NormalizedRecord.objects.get(id=record_id)

        if record.status == "LOCKED":
            return Response({"error": "Record is locked for audit"}, status=400)

        record.status = "APPROVED"
        record.save()

        AuditLog.objects.create(
            record=record,
            action="APPROVED",
            changed_by="Analyst"
        )

        return Response({"message": "Record approved"})


class RejectRecordView(APIView):
    def patch(self, request, record_id):
        record = NormalizedRecord.objects.get(id=record_id)

        if record.status == "LOCKED":
            return Response({"error": "Record is locked for audit"}, status=400)

        record.status = "REJECTED"
        record.save()

        AuditLog.objects.create(
            record=record,
            action="REJECTED",
            changed_by="Analyst"
        )

        return Response({"message": "Record rejected"})


class LockRecordView(APIView):
    def patch(self, request, record_id):
        record = NormalizedRecord.objects.get(id=record_id)

        record.status = "LOCKED"
        record.save()

        AuditLog.objects.create(
            record=record,
            action="LOCKED",
            changed_by="Analyst"
        )

        return Response({"message": "Record locked for audit"})