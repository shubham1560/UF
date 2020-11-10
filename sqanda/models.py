from django.db import models

# Create your models here.
from sys_user.models import SysUser


# class Question(models.Model):
#     pass


class Answer(models.Model):
    accepted = models.BooleanField()
    accepted_by = models.ForeignKey(SysUser, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    answer = models.TextField(null=True, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='answer_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='answer_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0, null=True, blank=True)


class Question(models.Model):
    accepted_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='answer_accepted_for_question')
    active = models.BooleanField(default=True)
    answer_count = models.IntegerField(default=0, null=True, blank=True)
    question = models.CharField(max_length=120, null=True, blank=True)
    question_details = models.TextField(null=True, blank=True)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='question_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='question_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)


class Comment(models.Model):
    active = models.BooleanField(default=True)
    comment = models.TextField(null=True, blank=True)
    table_id = models.CharField(max_length=10, blank=True, null=True)
    table_name = models.CharField(max_length=50, blank=True, null=True)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='comment_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='comment_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='tag_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='tag_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class ManyToManyTaggedObjects(models.Model):
    table_id = models.CharField(max_length=10, null=True, blank=True)
    table_name = models.CharField(max_length=50, null=True, blank=True)
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.CASCADE)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='m2m_tag_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='m2m_tag_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    active = models.BooleanField(default=True)
    table_id = models.CharField(max_length=10, null=True, blank=True)
    table_name = models.CharField(max_length=50, null=True, blank=True)
    up_vote = models.BooleanField(null=True, blank=True)
    sys_created_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='vote_created_by')
    sys_updated_by = models.ForeignKey(SysUser, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='vote_updated_by')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
