from django.contrib import admin
from . models import Account,Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','location']

# Register your models here.
admin.site.register(Account)
admin.site.register(Company,CompanyAdmin)
