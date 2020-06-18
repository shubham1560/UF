from django.contrib import admin
from .models import KbKnowledgeBase, KbCategory, KbKnowledge, KbFeedback, KbUse


# Register your models here.
class KbKnowledgeAdmin(admin.ModelAdmin):
    model = KbKnowledge
    list_display = ['id', 'title']


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


admin.site.register(KbCategory, KbCategoryAdmin)
admin.site.register(KbKnowledge, KbKnowledgeAdmin)
admin.site.register(KbKnowledgeBase, KbKnowledgeBaseAdmin)
admin.site.register(KbFeedback, KbFeedBackAdmin)



