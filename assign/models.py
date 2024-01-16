from django.db import models
from accounts.models import CustomUser
from device.models import Device

# Create your models here.
class AssignLog(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET('User removed'))
    took_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Log of {self.device} by {self.user}"
    
