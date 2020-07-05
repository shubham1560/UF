from django.contrib import admin
from .models import AttachedImage

# Register your models here.


class AttachedImagesAdmin(admin.ModelAdmin):
    model = AttachedImage
    list_display = ['id', 'real_image', 'thumbnail', 'compressed', 'article']


admin.site.register(AttachedImage, AttachedImagesAdmin)
