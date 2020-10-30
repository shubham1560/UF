from django.contrib import admin
from .models import Enhancement, Feature, Theme, Story, Epic, Defect, Sprint, StoryDependency, ScrumTask
# Register your models here.


class EnhancementAdmin(admin.ModelAdmin):
    model = Enhancement
    list_display = ['id', 'short_description', 'priority', 'state', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(EnhancementAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class EpicAdmin(admin.ModelAdmin):
    model = Epic
    list_display = ['id', 'short_description', 'priority', 'state', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(EpicAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class DefectAdmin(admin.ModelAdmin):
    model = Defect
    list_display = ['id', 'short_description', 'priority', 'state', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(DefectAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    list_display = ['id', 'short_description', 'priority', 'state', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(FeatureAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    list_display = ['id', 'theme', 'short_description', 'sys_created_by', 'sys_created_on']
    fields = ['theme', 'short_description', 'description']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(ThemeAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class StoryAdmin(admin.ModelAdmin):
    model = Story
    list_display = ['id', 'short_description', 'epic', 'state']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(StoryAdmin, self).save_model(request, obj, form, change)


class SprintAdmin(admin.ModelAdmin):
    model = Sprint
    list_display = ['id', 'short_description', 'priority', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(SprintAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class StoryDependencyAdmin(admin.ModelAdmin):
    model = StoryDependency
    list_display = ['id', 'dependent_story', 'prerequisite_story', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(StoryDependencyAdmin, self).save_model(request, obj, form, change)

    class Meta:
        ordering = ['sys_updated_on']


class ScrumTaskAdmin(admin.ModelAdmin):
    model = ScrumTask
    list_display = ['id', 'short_description', 'state', 'sys_created_by', 'sys_created_on']
    exclude = ['sys_created_on', 'sys_updated_by', 'sys_created_by']

    def save_model(self, request, obj, form, change):
        # obj.sys_created_by = request.user
        if obj.id:
            obj.sys_updated_by = request.user
        super(ScrumTaskAdmin, self).save_model(request, obj, form, change)

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

