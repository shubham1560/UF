from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .services import make_history_record
from .models import SysHistoryLine


class CreateHistoryRecord(APIView):

    def post(self, request, format=None):
        # breakpoint()
        result = make_history_record(request)
        return Response('record_created: ' + str(result), status=status.HTTP_201_CREATED)


class GetHistoryRecords(APIView):
    class HistorySerializer(serializers.ModelSerializer):
        class Meta:
            model = SysHistoryLine
            fields = ('sys_created_on', 'additional_comment', 'get_created_by')

    def get(self, request, record_id, record_type, format=None):
        record_table = ''
        if record_type == 'defect':
            record_table = 'Defect'
        if record_type == 'feature':
            record_table = 'Enhancement'
        try:
            comments = SysHistoryLine.objects.filter(table=record_table, table_sys_id=record_id).\
                order_by('-sys_created_on')
            result = self.HistorySerializer(comments, many=True)
        except ObjectDoesNotExist:
            return Response('', status=status.HTTP_200_OK)
        return Response(result.data, status=status.HTTP_200_OK)