from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
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

class ProfileView(DetailView):
    model = User
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_template_names(self):
        if self.object.user_type == 'customer':
            return ['users/customer_profile.html']
        else:
            return ['users/company_profile.html']
