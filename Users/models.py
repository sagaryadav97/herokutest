from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    username=models.CharField(max_length=150,null=False, blank=False,unique=True)
    password=models.CharField(max_length=150,null=False, blank=False)
    ROLE_CHOICES=(
        ('LIBRARIAN','LIBRARIAN'),
        ('MEMBER','MEMBER'),
    )
    Role=models.CharField(max_length=200,blank=False,null=False, choices=ROLE_CHOICES)
 
    
    USERNAME_FIELD="username"
    PASSWORD_FIELD="password"
    