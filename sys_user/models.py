from django.db import models
from django.contrib.auth.models import AbstractUser
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.files import File


def upload_path(instance, filename):
    return '/'.join(['profile_pic', str(instance.username), filename])


def upload_path_compress(instance, filename):
    return '/'.join(['profile_pic_compress', str(instance.username), filename])


def compressImage(uploadedImage):
    imageTemproary = Image.open(uploadedImage).convert('RGB')
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((200, 250))
    imageTemproaryResized.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


class SysUser(AbstractUser):

    USER_TPYE = [
        ('GU', 'GOOGLE'),
        ('RU', 'ROOT'),
        ('FU', 'FACEBOOK'),
    ]

    profile = models.ImageField(upload_to=upload_path, null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    header_image = models.ImageField(upload_to=upload_path_compress, null=True, blank=True)
    user_type = models.CharField(max_length=2, choices=USER_TPYE, default='RU')
    id_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    facebook_id = models.CharField(null=True, blank=True, max_length=100)
    facebook_profile_link = models.CharField(max_length=300, null=True, blank=True)
    public = models.BooleanField(default=True)
    instagram_profile_link = models.CharField(max_length=300, null=True, blank=True)
    twitter_profile_link = models.CharField(max_length=300, null=True, blank=True)
    external_website_link = models.CharField(max_length=300, null=True, blank=True)
    linkedin_profile = models.CharField(max_length=300, null=True, blank=True)
    password_needs_reset = models.BooleanField(default=False)
    is_trusted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # im = Image.open(self.featured_image).convert('RGB')
        # h, w = im.size
        # if h*w > 1000*1000:
        #     thumbnail = compress(self.featured_image, quality=1)
        #     self.featured_image_thumbnail = thumbnail
        # else:
        #     self.featured_image_thumbnail = self.featured_image
        # breakpoint()
        # im1 = Image.open(self.featured_image).convert('RGB').copy()
        # im_io = BytesIO()
        # im1.save(im_io, 'JPEG', quality=80)
        # new_image = File(im_io, name=self.featured_image.name)
        # im2 = im1.copy()
        # self.featured_image_thumbnail = image_optimizer(new_image,
        #                                                 output_size=(300, 200),
        #                                                 resize_method='cover')
        # breakpoint()
        if self.profile:
            self.header_image = compressImage(self.profile)
        # except FileNotFoundError:
        #     pass
        # self.featured_image = new_image
        super().save(*args, **kwargs)


class SubscriptionList(models.Model):
    email = models.EmailField(null=True, blank=True, max_length=200, unique=True)
    active = models.BooleanField(default=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)

