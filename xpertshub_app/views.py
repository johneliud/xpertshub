from django.contrib.auth.views import LogoutView
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'xpertshub_app/home.html')

class UserLogoutView(LogoutView):
    pass
