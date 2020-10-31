from agile_development.models import Enhancement, Defect
from .models import SysHistoryLine


def make_history_record(request):
    try:
        new_record = SysHistoryLine()
        if request.data['record_table'] == 'defect':
            new_record.table = 'Defect'
        if request.data['record_table'] == 'feature':
            new_record.table = 'Enhancement'
        new_record.additional_comment = request.data['comment']
        new_record.table_sys_id = request.data['record_id']
        new_record.sys_created_by = request.user
        new_record.save()
        return True
    except KeyError:
        return False

    # pass
