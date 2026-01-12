from django.urls import path
from .views import (CustomerRegisterView, CompanyRegisterView, UserLoginView, ProfileView,
                   select_user_type, set_user_type, complete_customer_profile, complete_company_profile)
from xpertshub_app.views import UserLogoutView

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/company/', CompanyRegisterView.as_view(), name='company_register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('select-user-type/', select_user_type, name='select_user_type'),
    path('set-user-type/', set_user_type, name='set_user_type'),
    path('complete-customer-profile/', complete_customer_profile, name='complete_customer_profile'),
    path('complete-company-profile/', complete_company_profile, name='complete_company_profile'),
]
