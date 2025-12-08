from django.urls import path
from .views import CustomerRegisterView, CompanyRegisterView, UserLoginView, ProfileView
from xpertshub_app.views import UserLogoutView

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/company/', CompanyRegisterView.as_view(), name='company_register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]
