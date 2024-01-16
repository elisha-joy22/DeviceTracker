from rest_framework import serializers
from device.models import Device
from assign.models import AssignLog


from datetime import datetime

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["brand","model_name","IMEI_number","status"]
    

class TakeDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["status","user"]



class ReturnDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["status","user"]


class DeviceLogSerializer(serializers.ModelSerializer):
    took_at = serializers.DateTimeField()
    returned_at = serializers.DateTimeField()
    
    class Meta:
        model = Device
        fields = ["brand","model_name","IMEI_number","took_at","returned_at"]

    def to_representation(self, instance):
        representation = {
            'device_name': instance[0] +" - "+ instance[1],
            'IMEI_number': instance[2],
            'took_at': instance[3],
            'returned_at': instance[4] if instance[4] else 'not_returned'
        }
        return representation

