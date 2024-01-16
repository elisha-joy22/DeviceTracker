from django.db import models
from accounts.models import CustomUser 


# Create your models here.
class Device(models.Model):
    STATUS_CHOICES = {
        'available':'Available',
        'in_use':'In use',
        'under_maintainance':'Under maintainance'
    }
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    IMEI_number = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.brand}-{self.model_name}"



