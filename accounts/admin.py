from django.contrib import admin

from accounts.models import CustomUser

admin.site.register(CustomUser)

admin.site.site_header = 'DeviceTracker Admin'           # default: "Django Administration"
admin.site.index_title = 'Control Panel'                 # default: "Site administration"
admin.site.site_title = 'DeviceTracker Admin'