import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Templates(UUIDMixin, TimeStampedMixin):
    title = models.CharField(max_length=50)
    template_text = models.TextField(_("email template"))
    author = models.CharField(max_length=50)

    class NotifType(models.TextChoices):
        email = _("email")
        push = _("push")
        sms = _("sms")

    type = models.TextField(_("type_notification"), choices=NotifType.choices)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "templates"
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")


class Tasks(UUIDMixin, TimeStampedMixin):
    template_id = models.ForeignKey(Templates, on_delete=models.CASCADE, related_name="template")
    task_name = models.CharField(max_length=50, default="Notification task")
    users_category = models.CharField(max_length=50)
    data = models.TextField(_("json"))
    pending_time = models.DateTimeField()

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = "tasks"
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
