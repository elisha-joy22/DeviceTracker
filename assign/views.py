from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from assign.models import AssignLog
from assign.serializer import AssignLogSerializer
from accounts.mixins import TokenAuthRequiredMixin


# Create your views here.
class AssignViewSet(TokenAuthRequiredMixin,GenericViewSet):
    queryset = AssignLog.objects.all()
    serializer_class = AssignLogSerializer
    
    def create(self,request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print("02")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success':serializer.data},status=status.HTTP_201_CREATED)
    
    def list(self,request):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response({'success':serializer.data},status=status.HTTP_200_OK)

    def retrieve(self,request,pk=None):
        item=self.get_object()
        serializer = self.get_serializer(item)
        return Response({'success':serializer.data},status=status.HTTP_200_OK)
    
    def destroy(self,request):
        item = self.get_object()
        item.delete()
        return Response({'success':'log_deleted'},status=status.HTTP_204_NO_CONTENT)


    @action(detail=False,methods=['get'])
    def user_device_log(self,request):
        user_log = AssignLog.objects.filter(
            user=request.user
        )
        serialised_user_log = AssignLogSerializer(user_log,many=True)
        return Response({'data':serialised_user_log.data})
