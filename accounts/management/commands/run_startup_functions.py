from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv
import os

load_dotenv()


class Command(BaseCommand):
    help = 'Prints'
    def handle(self,*args,**kwargs):
        create_superuser_default()  



def create_superuser_default():
    username = os.environ.get('DEFAULT_SUPERUSER_USERNAME')
    email = os.environ.get('DEFAULT_SUPERUSER_EMAIL')
    password = os.environ.get('DEFAULT_SUPERUSER_PASSWORD')

    if (existing_user:=User.objects.first()):
        print('Superuser already exists.')
    else:
        # Create a superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_staff=True
            )
            print('Superuser created during app startup.')
        except Exception as e:
            print("error:",e)

