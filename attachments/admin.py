from django.contrib import admin
from .models import AttachedImage

# Register your models here.


class AttachedImagesAdmin(admin.ModelAdmin):
    model = AttachedImage
    list_display = ['id',
                    'image_caption',
                    'real_image',
                    'compressed',
                    'table',
                    'table_id',
                    'sys_created_by',
                    'sys_created_on']
    sortable_by = ('sys_created_on', )
    list_filter = ('table',)


admin.site.register(AttachedImage, AttachedImagesAdmin)
