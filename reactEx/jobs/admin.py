from django.contrib import admin

from .models import Job, WorkShift, Position
# Register your models here.

admin.site.register(Job)
admin.site.register(WorkShift)
admin.site.register(Position)