from django import template
from services.models import ServiceRequest

register = template.Library()

@register.simple_tag
def get_pending_requests_count(user):
    """Get count of pending service requests for a company"""
    if user.is_authenticated and user.user_type == 'company':
        return ServiceRequest.objects.filter(
            service__company=user,
            service__status='approved'
        ).count()
    return 0
