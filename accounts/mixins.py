from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View 

class TokenAuthRequiredMixin:
    def dispatch(self,request,*args,**kwargs):
        print("TokenAuthRequiredMixin")
        if not request.user.is_authenticated:
            sign_url = reverse('oauth-start')
            return redirect(sign_url)
        return super().dispatch(request,*args,**kwargs)
    
