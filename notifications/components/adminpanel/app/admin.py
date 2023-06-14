from django.contrib import admin

from .models import Tasks, Templates

admin.site.register(Templates)
admin.site.register(Tasks)
