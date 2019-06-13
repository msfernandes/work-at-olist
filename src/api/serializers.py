from rest_framework.serializers import ModelSerializer
from core import models


class CallRecordSerializer(ModelSerializer):

    class Meta:
        model = models.CallRecord
        fields = (
            'id',
            'call_id',
            'record_type',
            'timestamp',
            'source',
            'destination',
        )
