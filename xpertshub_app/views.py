from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from services.views import get_most_requested_services
from users.models import User
from services.models import Service, ServiceRequest

# Create your views here.

def format_stat(count):
    """Format statistics with + suffix"""
    if count < 10:
        return "1+"
    elif count < 100:
        return f"{(count // 10) * 10}+"
    else:
        return f"{(count // 100) * 100}+"

def home(request):
    # Get database stats
    company_count = User.objects.filter(user_type='company').count()
    customer_count = User.objects.filter(user_type='customer').count()
    service_count = Service.objects.filter(status='approved').count()
    request_count = ServiceRequest.objects.count()
    
    context = {
        'featured_services': get_most_requested_services(),
        'stats': {
            'providers': format_stat(company_count),
            'customers': format_stat(customer_count),
            'services': format_stat(service_count),
            'requests': format_stat(request_count)
        }
    }
    return render(request, 'xpertshub_app/home.html', context)

def about(request):
    return render(request, 'xpertshub_app/about.html')

class UserLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
