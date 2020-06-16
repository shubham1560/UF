from django.contrib import admin
from .models import Email
# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    model = Email
    list_display = ["id", "description", "subject", "body", "footer", "priority"]


# Register your models here.
admin.site.register(Email, EmailAdmin)
