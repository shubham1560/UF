from django.db import models

# Create your models here.
from sys_user.models import SysUser
from knowledge.models import KbKnowledge, KbKnowledgeBase, KbCategory


# class Question(models.Model):
#     pass


class Answer(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
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
    id = models.CharField(primary_key=True, max_length=32)
    kb_base = models.ForeignKey(KbKnowledgeBase, on_delete=models.SET_NULL, null=True, blank=True)
    kb_category = models.ForeignKey(KbCategory, on_delete=models.SET_NULL, null=True, blank=True)
    kb_knowledge = models.ForeignKey(KbKnowledge, on_delete=models.SET_NULL, null=True, blank=True)
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
    question_url = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def get_kb_base(self):
        if self.kb_base:
            return {
                "label": self.kb_base.title,
                "id": self.kb_base.id,
            }
        else:
            return {}

    def get_kb_category(self):
        if self.kb_category:
            return {
                "label": self.kb_category.label,
                "id": self.kb_category.id
            }
        else:
            return {}

    def get_kb_knowledge(self):
        if self.kb_knowledge:
            return {
                "label": self.kb_knowledge.title,
                "id": self.kb_knowledge.id
            }
        else:
            return {}

    def get_created_by(self):
        if self.sys_created_by and self.sys_created_by.public and self.sys_created_by.is_active:
            return {
                'name': self.sys_created_by.first_name + " " + self.sys_created_by.last_name,
                'id': self.sys_created_by.id_name
            }
        else:
            return {}

    def get_updated_by(self):
        if self.sys_updated_by and self.sys_updated_by.public and self.sys_updated_by.is_active:
            return {
                'name': self.sys_updated_by.first_name + " " + self.sys_updated_by.last_name,
                'id': self.sys_updated_by.id_name
            }
        else:
            return {}


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
