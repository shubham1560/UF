from django.contrib import admin
from .models import Question, Answer, Tag, ManyToManyTaggedObjects, Vote, Comment


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['id', 'sys_created_on', 'sys_created_by']


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ['id', 'sys_created_on', 'sys_created_by']


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'sys_created_on', 'sys_created_by']


class ManyToManyTagAdmin(admin.ModelAdmin):
    model = ManyToManyTaggedObjects
    list_display = ['id', 'sys_created_on', 'sys_created_by']


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['id', 'sys_created_on', 'sys_created_by']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id', 'sys_created_on', 'sys_created_by']


admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ManyToManyTaggedObjects, ManyToManyTagAdmin)
