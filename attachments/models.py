from knowledge.models import KbKnowledge
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image, quality, name='test'):
    # breakpoint()
    im = Image.open(image).convert('RGB')
    h, w = im.size
    im_io = BytesIO()
    if h*w < 1000*1000:
        im.save(im_io, 'JPEG', quality=100)
    elif h*w < 3000*3000:
        if quality == "compress":
            im.save(im_io, 'JPEG', quality=60)
        else:
            im.save(im_io, 'JPEG', quality=10)
    elif h*w < 5000*5000:
        if quality == "compress":
            im.save(im_io, 'JPEG', quality=40)
        else:
            im.save(im_io, 'JPEG', quality=5)
    else:
        if quality == "compress":
            im.save(im_io, 'JPEG', quality=30)
        else:
            im.save(im_io, 'JPEG', quality=5)
    if name == 'test':
        new_image = File(im_io, name=image.name)
    else:
        new_image = File(im_io, name=(name+"_"+image.name))
    return new_image


class AttachedImage(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    image_caption = models.CharField(max_length=100, blank=True, null=True)
    real_image = models.ImageField(upload_to='articleimages/real_image/')
    thumbnail = models.ImageField(upload_to='articleimages/thumbnail/', blank=True, null=True)
    compressed = models.ImageField(upload_to='articleimages/compressed/', blank=True, null=True)
    featured_image = models.BooleanField(default=False)
    article = models.ForeignKey(KbKnowledge, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.article:
            compressed = compress(self.real_image, quality='compress', name=self.article.id)
            thumbnail = compress(self.real_image, quality='thumbnail', name=self.article.id)
        else:
            compressed = compress(self.real_image, quality='compress')
            thumbnail = compress(self.real_image, quality='thumbnail')
        self.compressed = compressed
        self.thumbnail = thumbnail
        super().save(*args, **kwargs)

