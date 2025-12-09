from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import ServiceCreationForm
from .models import Service

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
