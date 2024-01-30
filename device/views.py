from django.shortcuts import render,get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from device.models import Device
from assign.models import AssignLog
from accounts.models import CustomUser
from accounts.mixins import TokenAuthRequiredMixin
from device.serializer import DeviceSerializer,DeviceLogSerializer



# Create your views here.
class DeviceViewset(TokenAuthRequiredMixin,ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=False,methods=['get']) 
    def device_status(self,request):
        status = request.query_params.get('status')
        print(status)
        devices = Device.objects.filter(status=status)
        serializer = DeviceSerializer(devices,many=True)
        return Response({'success':serializer.data})

    

class DeviceActionViewSet(TokenAuthRequiredMixin,ViewSet):
    queryset = Device.objects.all()
    

    @action(detail=False, methods=['post'])
    def take_device(self, request):
        device_id = request.data.get('device')
        user_id = request.user.slack_id

        device_instance = get_object_or_404(Device, id=device_id)
        user_instance = get_object_or_404(CustomUser, slack_id=user_id)

        if device_instance.status == 'available':
            device_instance.user_id = user_id
            device_instance.status = 'in_use'
            device_instance.save()

            AssignLog.objects.create(
                device=device_instance,
                user=user_instance,
                took_at=timezone.now()
            )

            return Response(
                {"success": f"The device {device_instance.id} is allotted for user {device_instance.user_id}"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": f"The device {device_id} is not available right now!"},
                status=status.HTTP_400_BAD_REQUEST
            )
    

    @action(detail=False,methods=['post'])
    def return_device(self, request):
        device_id = request.data.get('device')
        user_id = request.user.slack_id
        device_instance = get_object_or_404(Device, id=device_id)

        if device_instance.user_id == user_id:
            device_instance.user_id = None
            device_instance.status = 'available'
            device_instance.save()

            assign_log_instance = AssignLog.objects.filter(
                device=device_id,
                user=user_id,
                returned_at=None
            ).first()
            
            if assign_log_instance:
                assign_log_instance.returned_at = timezone.now()
                assign_log_instance.save()

                return Response(
                    {"success": f"The device {device_instance.id} is returned by user {user_id}"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": f"No active assignment found for the device {device_id} by user {user_id}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": f"The device {device_id} can't be accessed right now or doesn't belong to the user!"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDevicesViewSet(TokenAuthRequiredMixin,ViewSet):
    queryset = Device.objects.all()

    def list(self,request):
        print("list")
        queryset = Device.objects.filter(user=request.user)
        serializer = DeviceSerializer(queryset,many=True)
        print("user-device-list")
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def history(self,request,user=None):
        print("history")
        queryset = AssignLog.objects.filter(user_id=request.user)\
                    .order_by('-returned_at')[:10]\
                    .values_list(
                        'device_id__brand',
                        'device_id__model_name',
                        'device_id__IMEI_number',
                        'took_at',
                        'returned_at'
                    )        
        serializer = DeviceLogSerializer(queryset,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)