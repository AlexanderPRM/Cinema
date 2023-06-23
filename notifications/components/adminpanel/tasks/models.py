import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationStatus(models.TextChoices):
    WAITING = "waiting"
    PROCESSING = "processing"
    DONE = "done"


class TaskTypes(models.TextChoices):
    NEW_EPISODES = "new_episodes"
    EMAIL_CONFIRM = "email_confirm"
    RECOMMENDATIONS = "recommendations"
    PERSON_LIKES = "person_likes"


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
    template_text = models.TextField(_("Notification Template"))
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


class UserTypes(models.TextChoices):
    ALL = "all"
    SELECTED = "selected"


class UsersCategories(UUIDMixin, TimeStampedMixin):
    category_name = models.CharField(max_length=50, choices=UserTypes.choices)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "users_categories"
        verbose_name = _("User Category")
        verbose_name_plural = _("Users Categories")


class Tasks(UUIDMixin, TimeStampedMixin):
    template_id = models.ForeignKey(Templates, on_delete=models.CASCADE, related_name="template")
    task_name = models.CharField(max_length=50, default="Notification task")
    task_type = models.CharField(
        max_length=50,
        choices=TaskTypes.choices,
        default=TaskTypes.NEW_EPISODES,
    )
    users_category = models.ForeignKey(
        UsersCategories, on_delete=models.CASCADE, related_name="users_category"
    )
    data = models.TextField(_("Data (json)"))
    pending_time = models.DateTimeField()
    send_status = models.CharField(
        max_length=50,
        choices=NotificationStatus.choices,
        default=NotificationStatus.WAITING,
    )

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = "tasks"
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


class UserMailingSubscribe(UUIDMixin):
    user_id = models.UUIDField(unique=True, null=False)

    def __str__(self):
        return f"{self.user_id} unsubscribe: {self.unsubscribe}"

    class Meta:
        db_table = "user_mailing_subscribe"
        verbose_name = _("UserSubscribe")
        verbose_name_plural = _("UsersSubscribes")
