from django.conf import settings
from rest_framework import exceptions

import os
import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv

from accounts.models import CustomUser

load_dotenv()

def generate_jwt(user):
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    jwt_algorithm = os.getenv('JWT_ALGORITHM')

    payload = {
        'user' : user['email'],
        'exp' : datetime.utcnow() + timedelta(days=1)
    }
    print("generating jwt...")
    jwt_token = jwt.encode(payload,jwt_secret,algorithm=jwt_algorithm)
    return jwt_token


def set_jwt_cookie(response, jwt_token):
    print('setting jwt cookie ...')
    response.set_cookie('auth_token', jwt_token, max_age=36000, httponly=True)
    return response


def authenticate_jwt(request):
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    jwt_algorithm = os.getenv('JWT_ALGORITHM')

    auth_token = request.COOKIES.get('auth_token') 
    print('provided_jwt',auth_token)

    if auth_token is None:
        return None       # No authentication header present
    print('po mone po')
    try:
        payload = jwt.decode(auth_token, jwt_secret, algorithms=[jwt_algorithm])
    except (ValueError, jwt.ExpiredSignatureError, jwt.DecodeError):
        raise exceptions.AuthenticationFailed('Invalid or expired token')

    user_email = payload.get('user')
    user = CustomUser.objects.get(email=user_email) 
    return user if user else None
