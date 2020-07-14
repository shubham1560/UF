from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from sys_user.models import SysUser
from io import BytesIO
from PIL import Image
from django.core.files import File
from image_optimizer.utils import image_optimizer
import sys
from django.core.exceptions import ObjectDoesNotExist
from decouple import config
from django.core.files.base import ContentFile


def compressImage(uploadedImage):
    imageTemproary = Image.open(uploadedImage).convert('RGB')
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((300, 200))
    imageTemproaryResized.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                         'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage


def compress(image, quality):
    im = Image.open(image).convert('RGB')
    # im = image
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=quality)
    new_image = File(im_io, name=image.name)
    return new_image


WORKFLOW_STATES = (
        ('draft', 'Draft'),
        ('review', 'Review'),
        ('published', 'Published'),
        ('retired', 'Retired'),
        ('outdated', 'Outdated'),
    )


class KbKnowledgeBase(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    sys_created_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    sys_updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='knowledge_base_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='knowledge_base_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Knowledge Bases"

    def __str__(self):
        return self.title


class KbCategory(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    label = models.CharField(max_length=20)
    parent_kb_base = models.ForeignKey(KbKnowledgeBase, blank=False, null=False, on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    sys_created_on = models.DateTimeField(auto_now=True)
    sys_updated_on = models.DateTimeField(auto_now_add=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='category_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='category_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Knowledge Categories"

    def __str__(self):
        return self.label


class KbKnowledge(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(KbCategory, on_delete=models.CASCADE, default='random')
    knowledge_base = models.ForeignKey(KbKnowledgeBase, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to="articles/featured_images/", blank=True, null=True)
    article_body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(SysUser,
                               on_delete=models.CASCADE,)
    featured_image_thumbnail = models.ImageField(upload_to="article/featured_image_thumbs/", blank=True, null=True)
    active = models.BooleanField(default=True)
    article_type = models.CharField(max_length=4, blank=True, null=True)
    disable_commenting = models.BooleanField(default=False)
    disable_suggesting = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    number = models.CharField(max_length=12, blank=True, null=True)
    published_on = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    parent_article = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')
    workflow = models.CharField(choices=WORKFLOW_STATES, max_length=10, blank=True, null=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='article_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='article_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Knowledge Articles"

    def __str__(self):
        return self.id

    def getAuthor(self):
        try:
            return {
                'author_exist': True,
                'first_name': self.author.first_name or '',
                "id": self.author.id_name or '',
                'last_name': self.author.last_name or '',
                'header_image': config('S3URL')+str(self.author.header_image) or '',
                'google_pic': self.author.profile_pic or '',
                'about': self.author.about or '',
            }
        except ObjectDoesNotExist:
            return {
                'author_exist': False
            }

    def get_category(self):
        try:
            return {
                'category_exist': True,
                'category_label': self.category.label,
                'id': self.category.id
            }
        except ObjectDoesNotExist:
            return{
                'category_exist': False,
            }

    def get_knowledge_base(self):
        try:
            return {
                'knowledge_base_exist': True,
                'knowledge_base': self.knowledge_base.title,
                'description': self.knowledge_base.description,
                'id': self.knowledge_base.id,
            }
        except ObjectDoesNotExist:
            return {
                'knowledge_base_exist': False,
            }

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
        if self.featured_image:
            self.featured_image_thumbnail = compressImage(self.featured_image)
        # self.featured_image = new_image
        super().save(*args, **kwargs)


class KbFeedback(models.Model):
    article = models.ForeignKey(KbKnowledge, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    rating = models.IntegerField(default=0)
    comments = models.TextField()
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Knowledge Feedbacks"

    def get_user(self):
        return {
            'first_name': self.user.first_name or '',
            "id": self.user.id_name or '',
            'last_name': self.user.last_name or '',
            'header_image': config('S3URL') + str(self.user.header_image) or '',
            'google_pic': self.user.profile_pic or '',
            'about': self.user.about or '',
        }

    def __str__(self):
        return self.comments


class KbUse(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE)
    useful = models.BooleanField(blank=True)
    viewed = models.BooleanField(blank=True)
    article = models.ForeignKey(KbKnowledge, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Knowledge Uses"
        unique_together = ['article', 'user']


class m2m_knowledge_feedback_likes(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey(KbFeedback, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(SysUser, on_delete=models.CASCADE)

    def asdict(self):
        return {"comment": self.comment, "liked_by": self.liked_by}

    class Meta:
        verbose_name_plural = "Knowledge Feedback Likes"
        unique_together = ['comment', 'liked_by']


class BookmarkUserArticle(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(KbKnowledge, on_delete=models.CASCADE)
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bookmarks User Articles"
        unique_together = ['article', 'user']

    def get_article(self):
        return {
            'id': self.article.id,
            'title': self.article.title,
            'description': self.article.description,
            'author': self.article.getAuthor(),

        }


