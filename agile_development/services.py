from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import status
from rest_framework.response import Response
from .models import Enhancement, Defect
from attachments.models import AttachedImage


def add_support(request):
    if request.data['record_type'] == 'feature':
        support = Enhancement()
    elif request.data['record_type'] == 'defect':
        support = Defect()
    else:
        return
    support.short_description = request.data["data"]['formdata']['short_description']
    support.description = request.data["data"]['formdata']['description']
    support.attached_images = request.data["data"]['attachments']
    support.sys_created_by = request.user
    support.state = 'draft'
    support.priority = '4'
    if request.user.groups.filter(name="Authors").exists():
        support.priority = '3'
    if request.user.groups.filter(name="Moderators").exists():
        support.priority = '2'
    support.save()
    save_the_attachments(request.data["data"]['attachments'], support.id)
    return support.id


def edit_support(request):
    if request.data['record_type'] == 'feature':
        try:
            support = Enhancement.objects.get(id=request.data['data']['id'])
        except ObjectDoesNotExist:
            return {'message': "not found", "status": status.HTTP_404_NOT_FOUND}
    elif request.data['record_type'] == 'defect':
        try:
            support = Defect.objects.get(id=request.data['data']['id'])
        except ObjectDoesNotExist:
            return {'message': "not found", "status": status.HTTP_404_NOT_FOUND}
    else:
        return {'message': "invalid request", "status": status.HTTP_404_NOT_FOUND}
    support.work_notes = request.data['data']['work_notes']
    support.state = request.data['data']['state']
    support.additional_comments = request.data['data']['additional_comments']
    support.save()
    return {"message": 'updated!', "status": status.HTTP_201_CREATED}


def save_the_attachments(attachments, record_id):
    for attachment in attachments:
        record = AttachedImage.objects.get(id=attachment['file']['id'])
        record.image_caption = attachment['file']['name']
        record.table_id = record_id
        record.save()


def get_support(request):
    # defects = Defect.objects.filter(sys_created_by=request.user).values('id',
    #                                                                     'short_description',
    #                                                                     'description',
    #                                                                     'state',
    #                                                                     'sys_created_on')
    # features = Enhancement.objects.filter(sys_created_by=request.user).values('id',
    #                                                                           'short_description',
    #                                                                           'description',
    #                                                                           'state',
    #                                                                           'sys_created_on')
    # for feature in features:
    #     feature['attachment'] = []
    #
    # for defect in defects:
    #     defect['attachment'] = []

    # breakpoint()
    pass


def get_ticket_detail(request, id, type):

    pass
