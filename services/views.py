from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Count
from .forms import ServiceCreationForm, ServiceRequestForm
from .models import Service, ServiceRequest

class CreateServiceView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceCreationForm
    template_name = 'services/create_service.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        # Only allow company users to create services
        if not request.user.is_authenticated or request.user.user_type != 'company':
            messages.error(request, 'Only companies can create services.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user
        messages.success(self.request, 'Service created successfully and is pending approval.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

class AllServicesView(ListView):
    model = Service
    template_name = 'services/all_services.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        return Service.objects.filter(status='approved').order_by('-date_created')

class ServicesByCategoryView(ListView):
    model = Service
    template_name = 'services/category_services.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        self.category = self.kwargs['field']
        return Service.objects.filter(status='approved', field=self.category).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related services in the same category (excluding current service)
        context['related_services'] = Service.objects.filter(
            status='approved',
            field=self.object.field
        ).exclude(id=self.object.id).order_by('-date_created')[:3]
        return context

class RequestServiceView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'services/request_service.html'

    def dispatch(self, request, *args, **kwargs):
        # Only allow customer users to request services
        if not request.user.is_authenticated or request.user.user_type != 'customer':
            messages.error(request, 'Only customers can request services.')
            return redirect('home')
        
        # Get the service being requested
        self.service = get_object_or_404(Service, pk=self.kwargs['service_id'], status='approved')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['service'] = self.service
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context

    def form_valid(self, form):
        form.instance.service = self.service
        form.instance.customer = self.request.user
        messages.success(self.request, f'Service request for "{self.service.name}" submitted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

def get_most_requested_services():
    """Helper function to get most requested services for home page"""
    return Service.objects.filter(status='approved').annotate(
        request_count=Count('requests')
    ).order_by('-request_count', '-date_created')[:6]
