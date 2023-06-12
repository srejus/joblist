from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100,null=True,blank=True)
    desc = models.TextField(null=True,blank=True)
    logo = models.ImageField(upload_to='company/logo/',null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    facebook_page = models.URLField(null=True,blank=True)
    linkedin = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True,blank=True)


class Account(AbstractUser):
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=150,null=True,blank=True)
    resume = models.FileField(upload_to='accounts/resume/',
                              validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
                              null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    tagline = models.CharField(max_length=100,null=True,blank=True)
    profile_picture = models.ImageField(upload_to='accounts/profiles/',null=True,blank=True)
    USER_TYPE_CHOICES = (
        ('personal','PERSONAL'),
        ('hr','HR')
    )
    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='personal')
    company = models.ForeignKey(Company,null=True,blank=True,on_delete=models.SET_NULL)