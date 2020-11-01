from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, status
from rest_framework.response import Response

from agile_development.models import Defect, Enhancement
from .services import make_history_record
from .models import SysHistoryLine


class CreateHistoryRecord(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        # breakpoint()
        result = make_history_record(request)
        return Response('record_created: ' + str(result), status=result["status"])


class GetHistoryRecords(APIView):
    permission_classes = (IsAuthenticated, )

    class HistorySerializer(serializers.ModelSerializer):
        class Meta:
            model = SysHistoryLine
            fields = ('sys_created_on', 'additional_comment', 'get_created_by')

    def get(self, request, record_id, record_type, format=None):
        record_table = ''
        if record_type == 'defect':
            record_table = 'Defect'
            table = Defect
        if record_type == 'feature':
            record_table = 'Enhancement'
            table = Enhancement
        if not request.user.is_staff:
            try:
                table.objects.get(id=record_id, sys_created_by=request.user)
            except ObjectDoesNotExist:
                return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
        try:
            comments = SysHistoryLine.objects.filter(table=record_table, table_sys_id=record_id).\
                order_by('-sys_created_on')
            result = self.HistorySerializer(comments, many=True)
        except ObjectDoesNotExist:
            return Response('', status=status.HTTP_200_OK)
        return Response(result.data, status=status.HTTP_200_OK)