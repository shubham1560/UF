from django.contrib import admin
from .models import KbKnowledgeBase, KbCategory, KbKnowledge, KbFeedback, KbUse,\
    m2m_knowledge_feedback_likes,BookmarkUserArticle
import binascii, os
import random


# Register your models here.
class KbKnowledgeAdmin(admin.ModelAdmin):
    model = KbKnowledge
    list_display = ['id', 'featured_image', 'featured_image_thumbnail', 'author', 'published_on',
                    'sys_created_on']
    fields = ['id', 'title', 'description', 'featured_image', 'author', 'knowledge_base', 'category', 'article_body']
    ordering = ['-sys_created_on']
    exclude = ['sys_created_by', 'sys_updated_by']

    def get_form(self, request, obj=None, **kwargs):
        form = super(KbKnowledgeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["id"].initial = "random"+str(random.randrange(10000, 100000))
        return form

    def save_model(self, request, obj, form, change):
        obj.sys_created_by = request.user
        if obj.id is None or 'random' in obj.id:
            obj.id = obj.title.lower().replace(" ", "-") + binascii.hexlify(os.urandom(4)).decode()
        if obj.id:
            obj.sys_updated_by = request.user
        super(KbKnowledgeAdmin, self).save_model(request, obj, form, change)


class KbKnowledgeBaseAdmin(admin.ModelAdmin):
    model = KbKnowledgeBase
    list_display = ['id', 'sys_created_by', 'sys_created_on', 'sys_updated_by']
    exclude = ['sys_created_by', 'sys_updated_by']

    def get_form(self, request, obj=None, **kwargs):
        form = super(KbKnowledgeBaseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["id"].initial = "random"+str(random.randrange(10000, 100000))
        return form

    def save_model(self, request, obj, form, change):
        # breakpoint()
        obj.sys_created_by = request.user
        if obj.id is None or "random" in obj.id:
            obj.id = obj.title.lower().replace(" ", "-") + "-" + binascii.hexlify(os.urandom(4)).decode()
        if obj.id:
            obj.sys_updated_by = request.user
        super(KbKnowledgeBaseAdmin, self).save_model(request, obj, form, change)


class KbCategoryAdmin(admin.ModelAdmin):
    model = KbCategory
    list_display = ['id', 'parent_kb_base', 'parent_category', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_by', 'sys_updated_by']

    def get_form(self, request, obj=None, **kwargs):
        form = super(KbCategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["id"].initial = "random"+str(random.randrange(10000, 100000))
        return form

    def save_model(self, request, obj, form, change):
        # breakpoint()
        obj.sys_created_by = request.user
        if obj.id is None or "random" in obj.id:
            obj.id = obj.label.lower().replace(" ", "-") + "-" + binascii.hexlify(os.urandom(4)).decode()
        if obj.id:
            obj.sys_updated_by = request.user
        super(KbCategoryAdmin, self).save_model(request, obj, form, change)


class KbFeedBackAdmin(admin.ModelAdmin):
    model = KbFeedback
    list_display = ['id']


class KbUseAdmin(admin.ModelAdmin):
    model = KbUse
    list_display = ['id', 'article']


class KbFeedbackLikesAdmin(admin.ModelAdmin):
    model = m2m_knowledge_feedback_likes
    list_display = ['id', 'comment', 'liked_by']


class BookmarkAdmin(admin.ModelAdmin):
    model = BookmarkUserArticle
    list_display = ['id', 'article', 'user', 'sys_created_on']


admin.site.register(KbCategory, KbCategoryAdmin)
admin.site.register(KbKnowledge, KbKnowledgeAdmin)
admin.site.register(KbKnowledgeBase, KbKnowledgeBaseAdmin)
admin.site.register(KbFeedback, KbFeedBackAdmin)
admin.site.register(KbUse, KbUseAdmin)
admin.site.register(m2m_knowledge_feedback_likes, KbFeedbackLikesAdmin)
admin.site.register(BookmarkUserArticle, BookmarkAdmin)



