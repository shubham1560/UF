from django.db import models
from sys_user.models import SysUser
from io import BytesIO
from PIL import Image
from django.core.files import File


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
    id = models.CharField(max_length=32, primary_key=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Knowledge Bases"


class KbCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    parent_kb_base = models.ForeignKey(KbKnowledgeBase, blank=False, null=False, on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    sys_created_on = models.DateTimeField(auto_now=True)
    sys_updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Knowledge Categories"


class KbKnowledge(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    active = models.BooleanField(default=True)
    article_type = models.CharField(max_length=4, blank=True, null=True)
    author = models.ForeignKey(SysUser,
                               on_delete=models.CASCADE,)
    category = models.ForeignKey(KbCategory, on_delete=models.CASCADE, blank=True, null=True)
    featured_image = models.ImageField(upload_to="articles/featured_images/", blank=True, null=True)
    featured_image_thumbnail = models.ImageField(upload_to="article/featured_image_thumbs/", blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    disable_commenting = models.BooleanField(default=False)
    disable_suggesting = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    knowledge_base = models.ForeignKey(KbKnowledgeBase, on_delete=models.CASCADE)
    number = models.CharField(max_length=12, blank=True, null=True)
    published_on = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    article_body = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    parent_article = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')
    workflow = models.CharField(choices=WORKFLOW_STATES, max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Knowledge Articles"

    def save(self, *args, **kwargs):
        im = Image.open(self.featured_image).convert('RGB')
        h, w = im.size
        if h*w > 1000*1000:
            thumbnail = compress(self.featured_image, quality=1)
            self.featured_image_thumbnail = thumbnail
        else:
            self.featured_image_thumbnail = self.featured_image
        super().save(*args, **kwargs)


class KbFeedback(models.Model):
    article = models.ForeignKey(KbKnowledge, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(default=0)
    comments = models.CharField(max_length=100)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Knowledge Feedbacks"

    def __str__(self):
        return "id: {}, comments:{},  user: {}".format(self.id,
                                                       self.comments,
                                                       self.user)


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


