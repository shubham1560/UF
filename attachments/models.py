from knowledge.models import KbKnowledge
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

from sys_user.models import SysUser


def upload_path(instance, filename):
    if instance.table:
        return '/'.join(['attachments', str(instance.table), 'real', filename])
    else:
        return '/'.join(['attachments', 'rogue', 'real', filename])


def upload_path_compress(instance, filename):
    if instance.table:
        return '/'.join(['attachments', str(instance.table), 'compress', filename])
    else:
        return '/'.join(['attachments', 'rogue', 'compressed', filename])


def compress(image, quality, name='test'):
    # breakpoint()
    im = Image.open(image).convert('RGB')
    h, w = im.size
    im_io = BytesIO()
    if h*w < 1000*1000:
        im.save(im_io, 'JPEG', quality=100)
    elif h*w < 3000*3000:
        im.save(im_io, 'JPEG', quality=60)
    elif h*w < 5000*5000:
        im.save(im_io, 'JPEG', quality=40)
    else:
        im.save(im_io, 'JPEG', quality=30)
    new_image = File(im_io, name=image.name)
    return new_image


class AttachedImage(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, blank=True, null=True)
    image_caption = models.CharField(max_length=100, blank=True, null=True)
    real_image = models.ImageField(upload_to=upload_path)
    thumbnail = models.ImageField(upload_to='articleimages/thumbnail/', blank=True, null=True)
    compressed = models.ImageField(upload_to=upload_path_compress, blank=True, null=True)
    real_image_size = models.CharField(max_length=20, blank=True, null=True)
    compressed_image_size = models.CharField(max_length=20, blank=True, null=True)
    # featured image going for the review from nsfw js
    flagged_image = models.BooleanField(default=False)
    table = models.CharField(max_length=100, null=True, blank=True)
    table_id = models.CharField(max_length=50, null=True, blank=True)
    article = models.ForeignKey(KbKnowledge, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # breakpoint()
        self.real_image_size = str(self.real_image.size/1000) + " KB"
        compressed = compress(self.real_image, quality="compress")
        self.compressed = compressed
        self.compressed_image_size = str(self.compressed.size/1000) + " KB"
        super().save(*args, **kwargs)



