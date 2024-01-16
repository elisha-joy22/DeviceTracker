from rest_framework import serializers
from assign.models import AssignLog


class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignLog
        fields = ['device','user']


class AssignLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignLog
        fields = '__all__'

    
