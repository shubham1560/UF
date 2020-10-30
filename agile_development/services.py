from rest_framework.views import status
from rest_framework.response import Response
from .models import Enhancement
from attachments.models import AttachedImage


def add_feature(request):
    enhancement = Enhancement()
    # breakpoint()
    enhancement.short_description = request.data['formdata']['short_description']
    enhancement.description = request.data['formdata']['description']
    enhancement.attached_images = request.data['attachments']
    enhancement.sys_created_by = request.user
    enhancement.state = 'draft'
    enhancement.priority = '4'
    if request.user.groups.filter(name="Authors").exists():
        enhancement.priority = '3'
    if request.user.groups.filter(name="Moderators").exists():
        enhancement.priority = '2'
    # enhancement.
    enhancement.save()
    save_the_attachments(request.data['attachments'], enhancement.id)
    # breakpoint()


def save_the_attachments(attachments, record_id):
    for attachment in attachments:
        record = AttachedImage.objects.get(id=attachment['file']['id'])
        record.image_caption = attachment['file']['name']
        record.table_id = record_id
        record.save()
