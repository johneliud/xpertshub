from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'xpertshub_app/home.html')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
