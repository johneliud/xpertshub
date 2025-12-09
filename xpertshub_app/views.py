from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from services.views import get_most_requested_services

# Create your views here.

def home(request):
    context = {
        'featured_services': get_most_requested_services()
    }
    return render(request, 'xpertshub_app/home.html', context)

class UserLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
