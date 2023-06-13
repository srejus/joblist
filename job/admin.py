from django.contrib import admin

from job.models import *

class JobAdmin(admin.ModelAdmin):
    list_display = ['id','title','company']


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id','job','applied_by']

# Register your models here.
admin.site.register(Job,JobAdmin)
admin.site.register(JobApplication,JobApplicationAdmin)
