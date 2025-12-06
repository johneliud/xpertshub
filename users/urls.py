from django.urls import path
from .views import CustomerRegisterView, CompanyRegisterView, UserLoginView

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/company/', CompanyRegisterView.as_view(), name='company_register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
