from django.contrib import admin

from job.models import *

class JobAdmin(admin.ModelAdmin):
    list_display = ['id','title','company']

# Register your models here.
admin.site.register(Job,JobAdmin)
