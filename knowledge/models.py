from django.db import models
from sys_user.models import SysUser
# Create your models here.

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
    article_type = models.CharField(max_length=4)
    author = models.ForeignKey(SysUser,
                               on_delete=models.CASCADE,)
    category = models.ForeignKey(KbCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    disable_commenting = models.BooleanField(default=False)
    disable_suggesting = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    knowledge_base = models.ForeignKey(KbKnowledgeBase, on_delete=models.CASCADE)
    number = models.CharField(max_length=12, unique=True)
    published_on = models.DateTimeField()
    rating = models.FloatField()
    title = models.CharField(max_length=50)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    article_body = models.TextField()
    topic = models.CharField(max_length=50)
    parent_article = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')
    workflow = models.CharField(choices=WORKFLOW_STATES, max_length=10)

    class Meta:
        verbose_name_plural = "Knowledge Articles"


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
    article = models.OneToOneField(KbKnowledge, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Knowledge Uses"