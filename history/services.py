from django.core.exceptions import ObjectDoesNotExist

from agile_development.models import Enhancement, Defect
from .models import SysHistoryLine
from rest_framework.views import status


def make_history_record(request):
    try:
        new_record = SysHistoryLine()
        if request.data['record_table'] == 'defect':
            new_record.table = 'Defect'
            table = Defect
            #staff waala code likhna hai idhar
        if request.data['record_table'] == 'feature':
            new_record.table = 'Enhancement'
            table = Enhancement
        if not request.user.is_staff:
            try:
                table.objects.get(id=request.data['record_id'], sys_created_by=request.user)
            except ObjectDoesNotExist:
                return {"status": status.HTTP_401_UNAUTHORIZED}
        new_record.additional_comment = request.data['comment']
        new_record.table_sys_id = request.data['record_id']
        new_record.sys_created_by = request.user
        new_record.save()
        return {"status": status.HTTP_201_CREATED}
    except KeyError:
        return {"status": status.HTTP_404_NOT_FOUND}

    # pass
