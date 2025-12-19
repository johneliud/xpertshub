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

@register.inclusion_tag('xpertshub_app/components/rating_display.html')
def show_rating(average_rating, rating_count, star_size="text-sm", text_size="text-sm", rating_text=""):
    """Display rating stars and count using the rating component"""
    return {
        'average_rating': average_rating,
        'rating_count': rating_count,
        'star_size': star_size,
        'text_size': text_size,
        'rating_text': rating_text,
    }
