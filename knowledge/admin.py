from django.contrib import admin
from .models import KbKnowledgeBase, KbCategory, KbKnowledge, KbFeedback, KbUse, m2m_knowledge_feedback_likes


# Register your models here.
class KbKnowledgeAdmin(admin.ModelAdmin):
    model = KbKnowledge
    list_display = ['id', 'featured_image', 'featured_image_thumbnail', 'author', 'published_on',
                    'sys_created_on']
    fields = ['id', 'title', 'featured_image', 'author', 'knowledge_base', 'article_body']
    ordering = ['-sys_created_on']


class KbKnowledgeBaseAdmin(admin.ModelAdmin):
    model = KbKnowledgeBase
    list_display = ['id']


class KbCategoryAdmin(admin.ModelAdmin):
    model = KbCategory
    list_display = ['id']


class KbFeedBackAdmin(admin.ModelAdmin):
    model = KbFeedback
    list_display = ['id']


class KbUseAdmin(admin.ModelAdmin):
    model = KbUse
    list_display = ['id', 'article']


class KbFeedbackLikesAdmin(admin.ModelAdmin):
    model = m2m_knowledge_feedback_likes
    list_display = ['id', 'comment', 'liked_by']


admin.site.register(KbCategory, KbCategoryAdmin)
admin.site.register(KbKnowledge, KbKnowledgeAdmin)
admin.site.register(KbKnowledgeBase, KbKnowledgeBaseAdmin)
admin.site.register(KbFeedback, KbFeedBackAdmin)
admin.site.register(KbUse, KbUseAdmin)
admin.site.register(m2m_knowledge_feedback_likes, KbFeedbackLikesAdmin)



