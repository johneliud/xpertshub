from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomerRegistrationForm, CompanyRegistrationForm, LoginForm
from .models import User

class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'users/customer_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = 'customer'
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(self.success_url)

class CompanyRegisterView(CreateView):
    model = User
    form_class = CompanyRegistrationForm
    template_name = 'users/company_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = 'company'
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(self.success_url)

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
