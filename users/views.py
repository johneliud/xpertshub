from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.decorators.http import require_http_methods
from .forms import (CustomerRegistrationForm, CompanyRegistrationForm, LoginForm,
                   CustomerProfileCompletionForm, CompanyProfileCompletionForm)
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

def select_user_type(request):
    return render(request, 'users/select_user_type.html')

@require_http_methods(["POST"])
def set_user_type(request):
    user_type = request.POST.get('user_type')
    if user_type in ['customer', 'company']:
        request.session['user_type'] = user_type
        return redirect(f'/accounts/google/login/?user_type={user_type}')
    return redirect('select_user_type')

@login_required
def complete_customer_profile(request):
    if request.user.user_type != 'customer':
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomerProfileCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerProfileCompletionForm(instance=request.user)
    
    return render(request, 'users/complete_customer_profile.html', {'form': form})

@login_required
def complete_company_profile(request):
    if request.user.user_type != 'company':
        return redirect('home')
    
    if request.method == 'POST':
        form = CompanyProfileCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CompanyProfileCompletionForm(instance=request.user)
    
    return render(request, 'users/complete_company_profile.html', {'form': form})
