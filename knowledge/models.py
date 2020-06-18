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


class KbCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    parent_category = models.ForeignKey('self', blank=True, null=True)
    parent_kb_base = models.ForeignKey('', blank=False, null=False)
    label = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    sys_created_on = models.DateTimeField(auto_now=True)
    sys_updated_on = models.DateTimeField(auto_now_add=True)


class KbKnowledge(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    active = models.BooleanField(default=True)
    article_type = models.CharField(max_length=4)
    author = models.ForeignKey(SysUser,
                               on_delete=models.CASCADE,)
    category = models.ForeignKey(KbKnowledgeBase, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    disable_commenting = models.BooleanField(default=False)
    disable_suggesting = models.BooleanField(deafult=False)
    flagged = models.BooleanField(default=False)
    knowledge_base = models.ForeignKey()
    number = models.CharField(max_length=12)
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
