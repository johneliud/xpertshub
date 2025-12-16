from django import forms
from .models import Service, ServiceRequest, Rating

class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'field', 'price_per_hour']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter service name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Describe your service',
                'rows': 4,
            }),
            'field': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'price_per_hour': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Restrict field choices based on company's field of work
        if self.user and self.user.user_type == 'company' and self.user.field_of_work != 'All in One':
            # Filter choices to only include company's field of work
            allowed_choices = [choice for choice in Service.FIELD_OF_WORK_CHOICES 
                             if choice[0] == self.user.field_of_work]
            self.fields['field'].choices = allowed_choices

    def clean_field(self):
        field = self.cleaned_data.get('field')
        
        # Validate field matches company's field of work (unless "All in One")
        if self.user and self.user.user_type == 'company':
            if self.user.field_of_work != 'All in One' and field != self.user.field_of_work:
                raise forms.ValidationError(
                    f"You can only create services in your field of work: {self.user.field_of_work}"
                )
        
        return field

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['address', 'service_time_hours']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your complete address',
                'rows': 3,
            }),
            'service_time_hours': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Estimated hours needed',
                'step': '0.5',
                'min': '0.5',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)

    def clean_service_time_hours(self):
        hours = self.cleaned_data.get('service_time_hours')
        if hours and hours < 0.5:
            raise forms.ValidationError("Minimum service time is 0.5 hours")
        return hours

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500',
            }),
            'review': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Share your experience (optional)',
                'rows': 4,
            }),
        }
