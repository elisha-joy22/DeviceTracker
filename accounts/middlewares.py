from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.middleware import get_user

from dotenv import load_dotenv
import jwt
import os

from accounts.models import CustomUser 
from accounts.auth_backends.CustomBackend import TokenBackend

load_dotenv()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("INside jwt middleware")
        token = request.COOKIES.get("auth_token")
        user = TokenBackend().authenticate(request,token=token)
        print("user exists?",user)
        print(request.user)
        request.user = SimpleLazyObject(
                            lambda: user if user else get_user(request)
        )   
