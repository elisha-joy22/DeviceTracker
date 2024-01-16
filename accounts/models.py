from django.db import models
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    def create_user(self, email, slack_id=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, slack_id=slack_id)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, slack_id=None):
        user = self.create_user(email, slack_id=slack_id)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, slack_id=None):
        user = self.create_user(email, slack_id=slack_id)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user




class CustomUser(models.Model):
    ROLE_CHOICES = [
        ('tester','Tester'),
        ('developer','Developer'),
        ('admin','Admin')
    ]

    slack_id = models.CharField(max_length=100,unique=True, db_index=True,primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES,null=True,blank=True)
    picture_url = models.CharField(max_length=200,blank=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.picture_url.endswith(".jpg"):
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
