from django.contrib import admin
from django.urls import path,include
from DeviceTracker.health_check import health_check


urlpatterns = [
    path('health',health_check,name="health_check"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('device/', include('device.urls')),
    path('assign/', include('assign.urls')),
]
