from rest_framework.views import status
from rest_framework.response import Response
from .models import Enhancement, Defect
from attachments.models import AttachedImage


def add_feature(request):
    # breakpoint()
    if request.data['record_type'] == 'feature':
        support = Enhancement()
    if request.data['record_type'] == 'defect':
        support = Defect()
    support.short_description = request.data["feature"]['formdata']['short_description']
    support.description = request.data["feature"]['formdata']['description']
    support.attached_images = request.data["feature"]['attachments']
    support.sys_created_by = request.user
    support.state = 'draft'
    support.priority = '4'
    if request.user.groups.filter(name="Authors").exists():
        support.priority = '3'
    if request.user.groups.filter(name="Moderators").exists():
        support.priority = '2'
    support.save()
    save_the_attachments(request.data["feature"]['attachments'], support.id)


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
