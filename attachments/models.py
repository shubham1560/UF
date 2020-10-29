from knowledge.models import KbKnowledge
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

from sys_user.models import SysUser


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
    real_image = models.ImageField(upload_to='articleimages/real_image/')
    thumbnail = models.ImageField(upload_to='articleimages/thumbnail/', blank=True, null=True)
    compressed = models.ImageField(upload_to='articleimages/compressed/', blank=True, null=True)
    featured_image = models.BooleanField(default=False)
    table = models.CharField(max_length=100, null=True, blank=True)
    table_id = models.CharField(max_length=50, null=True, blank=True)
    article = models.ForeignKey(KbKnowledge, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # breakpoint()
        compressed = compress(self.real_image, quality="compress")
        self.compressed = compressed
        super().save(*args, **kwargs)



