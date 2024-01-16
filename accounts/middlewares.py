from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404,redirect
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from utils.jwt import authenticate_jwt


from rest_framework import authentication


class TokenAuthenticationMiddleware:
    excluded_url_prefixes = ['/accounts/slack/','/admin/']

    def __init__(self,get_response):
        self.get_response = get_response

    def authenticate(self, request):            
        user = authenticate_jwt(request)
        if user==None:
            print("user None")
            return self.slack_authenticate(request)
        print(user)
        request.user = UserSerializer(user).data
        request.custom_user = UserSerializer(user).data
        #request.user.is_active = True 
        #request.user.is_authenticated = True              #Mandatory  .. I think for admin page - after running middleware its checking is_active is available on user 
        #print("Req.user",request.user)
        return self.get_response(request)


    def check_is_excluded_url(self,request):
        for excluded_url_prefix in TokenAuthenticationMiddleware.excluded_url_prefixes:
            if request.path.startswith(excluded_url_prefix):
                return True


    def slack_authenticate(self,request):
        print('inside slack_auth')
        return redirect('slack-install')


    def __call__(self,request):
        print("middleware_call")
        if self.check_is_excluded_url(request):
            print("45")
            return self.get_response(request)
        print("46")
        return self.authenticate(request)
        



class TestingMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print("test_middleware_call")
        print("Request",request)
        for attr in dir(request):
            if not attr.startswith('_'):
                #print(f"{attr}: {getattr(request, attr)}"
                pass
        return self.get_response(request)
