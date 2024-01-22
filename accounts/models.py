from django.db import models
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token


class CustomUser(models.Model):
    ROLE_CHOICES = [
        ('tester','Tester'),
        ('developer','Developer'),
        ('admin','Admin')
    ]

    slack_id = models.CharField(max_length=100,unique=True, db_index=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES,null=True,blank=True)
    picture_url = models.CharField(max_length=200,blank=True)

    def save(self, *args, **kwargs):
        if self.picture_url.endswith(".jpg"):
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name