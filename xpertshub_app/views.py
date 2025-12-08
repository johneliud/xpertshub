from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'xpertshub_app/home.html')

class UserLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
