from django.db import models

from accounts.models import Company,Account

# Create your models here.
class Job(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='job_company')
    title = models.CharField(max_length=200)
    JOB_TYPE_CHOICES = (
        ('on_site','ON SITE'),
        ('remote','REMOTE'),
        ('hybrid','HYBRID'),
    )
    job_type = models.CharField(max_length=50,choices=JOB_TYPE_CHOICES)
    experience = models.FloatField(default=0.0,verbose_name='Experience in Years')
    salary_from = models.FloatField()
    salary_upto = models.FloatField()
    posted_by = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,blank=True,related_name='job_posted_by')
    location = models.CharField(max_length=150)
    posted_time = models.DateTimeField(auto_now_add=True)
    no_of_applicants = models.IntegerField(default=0)
    JOB_STATUS_CHOICES = (
        ('draft','DRAFT'),
        ('open','OPEN'),
        ('closed','CLOSED')
    )
    job_status = models.CharField(max_length=50,choices=JOB_STATUS_CHOICES,default='open')
