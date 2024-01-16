from django.urls import path,include
from rest_framework.routers import DefaultRouter

from device.views import DeviceViewset,UserDevicesViewSet,DeviceActionViewSet

router = DefaultRouter()
router.register(r'device',DeviceViewset,basename='device')
router.register(r'user_device',UserDevicesViewSet,basename='user_device')
router.register(r'device_action',DeviceActionViewSet,basename='device_action')

urlpatterns = router.urls

#urlpatterns = [
#    path('',include(router.urls)),
#]
