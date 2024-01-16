from django.urls import path,include
from rest_framework.routers import DefaultRouter
from assign.views import AssignViewSet

router = DefaultRouter()
router.register(r'',AssignViewSet)

urlpatterns = [
    path('',include(router.urls))
]
