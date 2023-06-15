from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Tasks, Templates, UsersCategories


class TemplatesInline(SummernoteModelAdmin):
    list_display = ("title", "type")
    summernote_fields = ("template_text",)


class TesksInline(SummernoteModelAdmin):
    list_display = (
        "task_name",
        "users_category",
        "pending_time",
    )
    summernote_fields = ("data",)


admin.site.register(Templates, TemplatesInline)
admin.site.register(Tasks, TesksInline)
admin.site.register(UsersCategories)
