from django.contrib import admin

from django.contrib import admin
from django.utils import timezone
from .models import Service, ServiceRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'field', 'price_per_hour', 'status', 'date_created']
    list_filter = ['status', 'field', 'date_created']
    search_fields = ['name', 'company__username', 'company__email']
    readonly_fields = ['date_created', 'date_approved', 'approved_by']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'field', 'price_per_hour', 'company')
        }),
        ('Approval Status', {
            'fields': ('status', 'approved_by', 'date_approved')
        }),
        ('Timestamps', {
            'fields': ('date_created',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Auto-set approval fields when status changes to approved
        if change and obj.status == 'approved' and not obj.approved_by:
            obj.approved_by = request.user
            obj.date_approved = timezone.now()
        super().save_model(request, obj, form, change)

    actions = ['approve_services', 'reject_services']

    def approve_services(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user,
            date_approved=timezone.now()
        )
        self.message_user(request, f'{updated} services approved successfully.')
    approve_services.short_description = "Approve selected services"

    def reject_services(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} services rejected.')
    reject_services.short_description = "Reject selected services"

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['service', 'customer', 'calculated_cost', 'date_requested']
    list_filter = ['date_requested', 'service__field']
    search_fields = ['service__name', 'customer__username', 'customer__email']
    readonly_fields = ['calculated_cost', 'date_requested']
