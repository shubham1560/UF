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
    (1, '1 - Critical'),
    (2, '2 - High'),
    (3, '3 - Moderate'),
    (4, '4 - Low'),
    (5, '5 - Planning')
)

TASK_TYPE = (
    ('analysis', 'Analysis'),
    ('coding', 'Coding'),
    ('testing', 'Testing'),
)


class Feature(models.Model):
    priority = models.CharField(choices=PRIORITY, blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    work_notes = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class Defect(Feature):
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='D')


class Enhancement(Feature):
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='EN')


class Epic(Feature):
    feature_type = models.CharField(choices=FEATURE_TYPE, max_length=5, default='EP')


class Sprint(models.Model):
    priority = models.CharField(choices=PRIORITY, max_length=1, blank=True, null=True)
    state = models.CharField(choices=SPRINT_STATES, max_length=50, blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    work_notes = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    planned_start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class Theme(models.Model):
    theme = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=400, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class Story(Feature):
    points = models.IntegerField(default=5, blank=True, null=True)
    blocked = models.BooleanField(default=False, blank=True, null=True)
    reason_of_blockage = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(choices=STORY_STATES, max_length=50, blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True)
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE, blank=True, null=True)
    enhancement = models.ForeignKey(Enhancement, on_delete=models.CASCADE, blank=True, null=True)
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE, blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class StoryDependency(models.Model):
    dependent_story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    prerequisite_story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)


class ScrumTask(models.Model):
    start_date = models.DateField( blank=True, null=True)
    end_date = models.DateField( blank=True, null=True)
    remaining_hours = models.CharField(max_length=40, blank=True, null=True)
    percent_complete = models.IntegerField( blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    type = models.CharField(choices=TASK_TYPE, max_length=50,  blank=True, null=True)
    blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=300, blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    assigned_to = models.ForeignKey(SysUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},  blank=True, null=True)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE,  blank=True, null=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    close_notes = models.TextField( blank=True, null=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)




