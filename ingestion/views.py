import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from tenants.models import Tenant
from ingestion.models import DataSource, RawRecord
from normalization.models import NormalizedRecord
from .serializers import FileUploadSerializer


class SAPUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        tenant = Tenant.objects.get(id=serializer.validated_data["tenant_id"])
        uploaded_by = serializer.validated_data["uploaded_by"]
        file = serializer.validated_data["file"]

        df = pd.read_csv(file).fillna("")
        df.columns = df.columns.str.strip()

        data_source = DataSource.objects.create(
            tenant=tenant,
            source_type="SAP",
            file_name=file.name,
            uploaded_by=uploaded_by,
        )

        created_count = 0

        for _, row in df.iterrows():
            raw = RawRecord.objects.create(
                data_source=data_source,
                raw_payload=dict(row),
                validation_status="VALID"
            )

            try:
                quantity = float(row.iloc[3])
                unit = str(row.iloc[4]).lower()

                if unit == "gallons":
                    normalized_value = quantity * 3.78541
                    normalized_unit = "liters"
                else:
                    normalized_value = quantity
                    normalized_unit = "liters"

                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type="Fuel",
                    scope="SCOPE_1",
                    original_value=quantity,
                    original_unit=unit,
                    normalized_value=normalized_value,
                    normalized_unit=normalized_unit,
                    suspicious=normalized_value > 10000,
                    status="PENDING"
                )

            except Exception:
                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type="Fuel",
                    scope="SCOPE_1",
                    original_value=0,
                    original_unit="unknown",
                    normalized_value=0,
                    normalized_unit="unknown",
                    suspicious=True,
                    status="FAILED"
                )

            created_count += 1

        return Response({
            "message": "SAP uploaded successfully",
            "rows_processed": created_count
        }, status=201)


class UtilityUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        tenant = Tenant.objects.get(id=serializer.validated_data["tenant_id"])
        uploaded_by = serializer.validated_data["uploaded_by"]
        file = serializer.validated_data["file"]

        df = pd.read_csv(file).fillna("")
        df.columns = df.columns.str.strip()

        data_source = DataSource.objects.create(
            tenant=tenant,
            source_type="UTILITY",
            file_name=file.name,
            uploaded_by=uploaded_by,
        )

        created_count = 0

        for _, row in df.iterrows():
            raw = RawRecord.objects.create(
                data_source=data_source,
                raw_payload=dict(row),
                validation_status="VALID"
            )

            try:
                consumption = float(row.iloc[3])
                unit = str(row.iloc[4]).lower()

                if unit == "mwh":
                    normalized_value = consumption * 1000
                    normalized_unit = "kwh"
                else:
                    normalized_value = consumption
                    normalized_unit = "kwh"

                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type="Electricity",
                    scope="SCOPE_2",
                    original_value=consumption,
                    original_unit=unit,
                    normalized_value=normalized_value,
                    normalized_unit=normalized_unit,
                    suspicious=normalized_value > 50000,
                    status="PENDING"
                )

            except Exception:
                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type="Electricity",
                    scope="SCOPE_2",
                    original_value=0,
                    original_unit="unknown",
                    normalized_value=0,
                    normalized_unit="unknown",
                    suspicious=True,
                    status="FAILED"
                )

            created_count += 1

        return Response({
            "message": "Utility uploaded successfully",
            "rows_processed": created_count
        }, status=201)


class TravelUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        tenant = Tenant.objects.get(id=serializer.validated_data["tenant_id"])
        uploaded_by = serializer.validated_data["uploaded_by"]
        file = serializer.validated_data["file"]

        df = pd.read_csv(file).fillna("")
        df.columns = df.columns.str.strip()

        data_source = DataSource.objects.create(
            tenant=tenant,
            source_type="TRAVEL",
            file_name=file.name,
            uploaded_by=uploaded_by,
        )

        created_count = 0

        for _, row in df.iterrows():
            raw = RawRecord.objects.create(
                data_source=data_source,
                raw_payload=dict(row),
                validation_status="VALID"
            )

            try:
                category = str(row.iloc[2])
                distance = float(row.iloc[5])
                unit = str(row.iloc[6]).lower()

                if unit == "miles":
                    normalized_value = distance * 1.60934
                    normalized_unit = "km"
                else:
                    normalized_value = distance
                    normalized_unit = "km"

                suspicious = (
                    category.lower() == "flight" and normalized_value == 0
                )

                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type=category,
                    scope="SCOPE_3",
                    original_value=distance,
                    original_unit=unit,
                    normalized_value=normalized_value,
                    normalized_unit=normalized_unit,
                    suspicious=suspicious,
                    status="PENDING"
                )

            except Exception:
                NormalizedRecord.objects.create(
                    tenant=tenant,
                    raw_record=raw,
                    activity_type="Travel",
                    scope="SCOPE_3",
                    original_value=0,
                    original_unit="unknown",
                    normalized_value=0,
                    normalized_unit="unknown",
                    suspicious=True,
                    status="FAILED"
                )

            created_count += 1

        return Response({
            "message": "Travel uploaded successfully",
            "rows_processed": created_count
        }, status=201)