from django.db.models.signals import post_save
from django.dispatch import receiver
from assign.models import AssignLog

'''
@receiver(post_save,sender=AssignLog)
def update_device(sender,instance,**kwargs):
    device = instance.device
    device.user = instance.user
    device.status = 'in_use'
    device.save()
'''