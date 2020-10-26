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
from django.core.cache import cache
from django.core.files.base import ContentFile
from uFraudApi.settings.base import CACHE_KEY


def compressImage(uploadedImage):
    imageTemproary = Image.open(uploadedImage).convert('RGB')
    outputIoStream = BytesIO()
    imageTemproaryResized = imageTemproary.resize((200, 200))
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
    order = models.IntegerField(null=True, blank=True)
    real_image = models.ImageField(upload_to="knowledge_base/real_images/", null=True, blank=True)
    compressed_image = models.ImageField(upload_to="knowledge_base/compressed_images/", null=True, blank=True)
    sys_updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='knowledge_base_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='knowledge_base_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Knowledge Bases"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        cache.delete(CACHE_KEY+".kb_bases")
        if self.real_image:
            self.compressed_image = compressImage(self.real_image)
        super().save(*args, **kwargs)


class KbCategory(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    label = models.CharField(max_length=100)
    parent_kb_base = models.ForeignKey(KbKnowledgeBase, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="related_categories")
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                        related_name="parent_of_category")
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    course = models.BooleanField(default=False, null=True, blank=True)
    section = models.BooleanField(default=False, null=True, blank=True)
    active = models.BooleanField(default=True)
    real_image = models.ImageField(upload_to="knowledge_base/real_images/", null=True, blank=True)
    compressed_image = models.ImageField(upload_to="knowledge_base/compressed_images/", null=True, blank=True)
    sys_updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    sys_created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='category_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='category_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Knowledge Categories"

    def __str__(self):
        fin_str = ""
        if self.course:
            fin_str += "course: " + self.label
        elif self.section:
            fin_str += "section: " + self.label + ", course: " + self.parent_category.label
        else:
            fin_str += "Branch: " + self.label
        return fin_str

    def get_parent_category(self):
        if self.parent_category:
            return {
                "label": self.parent_category.label,
                'description': self.parent_category.description
            }
        return {
            "label": "root"
        }

    def get_parent_knowledgebase(self):
        return{
            "label": self.parent_kb_base.title,
            "description": self.parent_kb_base.description
        }

    def get_created_by(self):
        if self.sys_created_by:
            return {
                "author": self.sys_created_by.email
            }

    def get_first_article(self):
        article = KbKnowledge.objects.filter(category=self).order_by('order')[0:1]
        # breakpoint()
        if article:
            return {
                "first_article_id": article[0].id
            }
        else:
            return {
                "first_article_id" : ''
            }

    def save(self, *args, **kwargs):
        cache.clear()
        if self.real_image:
            self.compressed_image = compressImage(self.real_image)
        super().save(*args, **kwargs)


class KnowledgeSection(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=100)
    course = models.ForeignKey(KbCategory,
                               on_delete=models.CASCADE,
                               limit_choices_to={'course': True},
                               related_name="related_sections")
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.course.label + " > " + self.label


class KbKnowledge(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(KbCategory, on_delete=models.CASCADE,
                                 limit_choices_to={'course': True},
                                 # default='random',
                                 related_name="article_category",
                                 null=True, blank=True)
    knowledge_base = models.ForeignKey(KbKnowledgeBase, on_delete=models.CASCADE, related_name="article_kb_base")
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to="articles/featured_images/", blank=True, null=True)
    article_body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(SysUser,
                               on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(KnowledgeSection, on_delete=models.CASCADE, related_name="related_articles",
                                null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
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
    view_count_logged_in = models.IntegerField(default=0, blank=True, null=True)
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
            if self.author:
                if self.author.public:
                    return {
                        'author_exist': True,
                        'first_name': self.author.first_name or '',
                        "id": self.author.id_name or '',
                        'last_name': self.author.last_name or '',
                        'header_image': config('S3URL')+str(self.author.header_image) or '',
                        'google_pic': self.author.profile_pic or '',
                        'about': self.author.about or '',
                        'facebook_link': self.author.facebook_profile_link or '',
                        'instagram_link': self.author.instagram_profile_link or '',
                        'linkedin_link': self.author.linkedin_profile or '',
                        'external_website_link': self.author.external_website_link or '',
                        'twitter_link': self.author.twitter_profile_link or ''
                    }
                else:
                    return {

                    }
            else:
                return {
                    # 'about': self.author.about or '',
                }
        except ObjectDoesNotExist:
            return {
                'author_exist': False
            }

    def get_category(self):
        if self.category:
            try:
                return {
                    'category_exist': True,
                    'category_label': self.category.label or '',
                    'id': self.category.id or ''
                }
            except ObjectDoesNotExist:
                return{
                    'category_exist': False,
                }
        else:
            return {
                'category_exist': False,
            }

    def get_knowledge_base(self):
        try:
            return {
                'knowledge_base_exist': True,
                'knowledge_base': self.knowledge_base.title or '',
                'description': self.knowledge_base.description or '',
                'id': self.knowledge_base.id or '',
            }
        except ObjectDoesNotExist:
            return {
                'knowledge_base_exist': False,
            }

    def save(self, *args, **kwargs):
        cache.clear()
        if self.featured_image:
            self.featured_image_thumbnail = compressImage(self.featured_image)
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
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, related_name='user_activity')
    course = models.ForeignKey(KbCategory,
                               null=True,
                               blank=True,
                               related_name='course_kb_category',
                               on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    percentage_completed = models.IntegerField(null=True, blank=True)
    useful = models.BooleanField(blank=True, null=True)
    viewed = models.BooleanField(blank=True, null=True)
    article = models.ForeignKey(KbKnowledge, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Knowledge Uses"
        unique_together = ['article', 'user', 'course']


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
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, related_name='user_bookmark')

    class Meta:
        verbose_name_plural = "Bookmarks User Articles"
        unique_together = ['article', 'user']

    def get_article(self):
        if self.article.section:
            return {
                'id': self.article.id or '',
                'title': self.article.title or '',
                # 'description': self.article.description or '',
                # 'author': self.article.getAuthor() or '',
                'course_id': self.article.section.course.id or '',
                'course_label': self.article.section.course.label or '',
                'kb_base_label': self.article.knowledge_base.title or '',
                # 'kb_base_id': self.article.knowledge_base.title or ''

            }
        else:
            return {
                'id': self.article.id or '',
                'title': self.article.title or '',
                # 'description': self.article.description or '',
                # 'author': self.article.getAuthor() or '',
                # 'course_id': self.article.section.course.id or '',
                # 'course_label': self.article.section.course.label or ''
            }

