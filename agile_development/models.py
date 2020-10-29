from django.db import models
from sys_user.models import SysUser
from django.contrib.auth.models import Group


# Create your models here.

FEATURE_TYPE = (
    ('D', 'Defect'),
    ('EN', 'Enhancement'),
    ('EP', 'Epic')
)


STORY_STATES = (
    ('draft', 'Draft'),
    ('ready', 'Ready'),
    ('wip', "Work in Progress"),
    ('rft', 'Ready for Testing'),
    ('complete', "Complete"),
    ('cancelled', "Cancelled")
)


STATES = (
    ('draft', 'Draft'),
    ('planning', 'Planning'),
    ('wip', 'Work in Progress'),
    ('complete', 'Complete'),
    ('cancelled', 'Cancelled')
)

SPRINT_STATES = (
    ('draft', 'Draft'),
    ('planning', 'Planning'),
    ('current', 'Current'),
    ('complete', 'Complete'),
    ('cancelled', 'Cancelled')
)

PRIORITY = (
    ('1', '1 - Critical'),
    ('2', '2 - High'),
    ('3', '3 - Moderate'),
    ('4', '4 - Low'),
    ('5', '5 - Planning')
)

TASK_TYPE = (
    ('analysis', 'Analysis'),
    ('coding', 'Coding'),
    ('testing', 'Testing'),
)

def upload_path(instance, filename):
    return '/'.join(['story_images', str(instance.id), filename])


class Feature(models.Model):
    priority = models.CharField(choices=PRIORITY, blank=True, null=True, max_length=30)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    attached_images = models.TextField(blank=True, null=True)
    work_notes = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='feature_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='feature_updated_by', limit_choices_to={'is_staff': True})

    def __str__(self):
        return self.short_description


class Defect(Feature):
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='D')


class Enhancement(Feature):
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='EN')


class Epic(Feature):
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='EP')


class Sprint(models.Model):
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(choices=PRIORITY, max_length=1, blank=True, null=True)
    state = models.CharField(choices=SPRINT_STATES, max_length=50, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    work_notes = models.TextField(blank=True, null=True)
    planned_start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='sprint_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='sprint_updated_by', limit_choices_to={'is_staff': True})

    def __str__(self):
        self.short_description


class Theme(models.Model):
    theme = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=400, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='updated_by', limit_choices_to={'is_staff': True})

    def save(self, *args, **kwargs):
        # breakpoint()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_description


class Story(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True)
    priority = models.CharField(choices=PRIORITY, blank=True, null=True, max_length=30)
    state = models.CharField(choices=STORY_STATES, max_length=50, blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    attached_image1 = models.ImageField(null=True, blank=True, upload_to=upload_path)
    attached_image2 = models.ImageField(null=True, blank=True, upload_to=upload_path)
    attached_image3 = models.ImageField(null=True, blank=True, upload_to=upload_path)
    attached_image4 = models.ImageField(null=True, blank=True, upload_to=upload_path)
    attached_image5 = models.ImageField(null=True, blank=True, upload_to=upload_path)
    work_notes = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True,
                                    null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    points = models.IntegerField(default=5, blank=True, null=True)
    blocked = models.BooleanField(default=False, blank=True, null=True)
    reason_of_blockage = models.CharField(max_length=100, blank=True, null=True)
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE, blank=True, null=True, related_name='defects')
    enhancement = models.ForeignKey(Enhancement, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='enhancements')
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE, blank=True, null=True, related_name='epics')
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='story_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='story_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.short_description


class StoryDependency(models.Model):
    dependent_story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    prerequisite_story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True,
                                           related_name='prerequisite')
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='dependency_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='dependency_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Story Dependencies"


class ScrumTask(models.Model):
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    type = models.CharField(choices=TASK_TYPE, max_length=50,  blank=True, null=True)
    close_notes = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    remaining_hours = models.CharField(max_length=40, blank=True, null=True)
    percent_complete = models.IntegerField( blank=True, null=True)
    blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=300, blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},  blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE,  blank=True, null=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='task_created_by', limit_choices_to={'is_staff': True})
    sys_updated_by = models.ForeignKey(SysUser, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='task_updated_by', limit_choices_to={'is_staff': True})

    class Meta:
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.short_description




