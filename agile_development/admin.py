from django.contrib import admin
from .models import Enhancement, Feature, Theme, Story, Epic, Defect, Sprint, StoryDependency, ScrumTask
# Register your models here.


class EnhancementAdmin(admin.ModelAdmin):
    model = Enhancement
    list_display = ['id', 'short_description', 'priority', 'state']

    class Meta:
        ordering = ['sys_updated_on']


class EpicAdmin(admin.ModelAdmin):
    model = Epic
    list_display = ['id', 'short_description', 'priority', 'state']

    class Meta:
        ordering = ['sys_updated_on']


class DefectAdmin(admin.ModelAdmin):
    model = Defect
    list_display = ['id', 'short_description', 'priority', 'state']

    class Meta:
        ordering = ['sys_updated_on']


class FeatureAdmin(admin.ModelAdmin):
    model = Feature

    class Meta:
        ordering = ['sys_updated_on']


class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    list_display = ['id', 'theme', 'short_description', 'description', 'sys_created_by', 'sys_updated_by']
    fields = ['theme', 'short_description', 'description', 'sys_created_by', 'sys_updated_by']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ThemeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["sys_created_by"].initial = request.user
        try:
            if obj.id:
                obj.sys_updated_by = request.user
        except AttributeError:
            pass
        return form

    class Meta:
        ordering = ['sys_updated_on']


class StoryAdmin(admin.ModelAdmin):
    model = Story
    list_display = ['id', 'short_description', 'epic', 'state']

    class Meta:
        verbose_name_plural = "Stories"

    def get_form(self, request, obj=None, **kwargs):
        form = super(StoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["sys_created_by"].initial = request.user
        try:
            if obj.id:
                obj.sys_updated_by = request.user
        except AttributeError:
            pass
        return form


class SprintAdmin(admin.ModelAdmin):
    model = Sprint

    class Meta:
        ordering = ['sys_updated_on']


class StoryDependencyAdmin(admin.ModelAdmin):
    model = StoryDependency

    class Meta:
        verbose_name_plural = "Story Dependencies"
        ordering = ['sys_updated_on']


class ScrumTaskAdmin(admin.ModelAdmin):
    model = ScrumTask

    class Meta:
        ordering = ['sys_updated_on']


admin.site.register(Enhancement, EnhancementAdmin)
# admin.site.register(Feature, FeatureAdmin)
admin.site.register(Defect, DefectAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Epic, EpicAdmin)
admin.site.register(ScrumTask, ScrumTaskAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(StoryDependency, StoryDependencyAdmin)

