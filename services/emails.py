from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def send_request_confirmation_email(service_request):
    """Send confirmation email to customer after service request"""
    try:
        customer = service_request.customer
        service = service_request.service
        
        context = {
            'customer_name': customer.username,
            'service_name': service.name,
            'service_field': service.field,
            'company_name': service.company.username,
            'address': service_request.address,
            'service_hours': service_request.service_time_hours,
            'calculated_cost': service_request.calculated_cost,
            'date_requested': service_request.date_requested.strftime('%B %d, %Y at %I:%M %p'),
            'profile_url': f"{settings.SITE_URL}/auth/profile/{customer.username}/" if hasattr(settings, 'SITE_URL') else '#'
        }
        
        html_message = render_to_string('services/emails/request_confirmation.html', context)
        
        # Use SendGrid Web API in production, SMTP in development
        if not settings.DEBUG and hasattr(settings, 'SENDGRID_API_KEY') and settings.SENDGRID_API_KEY:
            return send_sendgrid_email(
                to_email=customer.email,
                subject=f'Service Request Confirmed - {service.name}',
                html_content=html_message
            )
        else:
            send_mail(
                subject=f'Service Request Confirmed - {service.name}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer.email],
                html_message=html_message,
                fail_silently=True,
            )
        
        logger.info(f"Confirmation email sent to {customer.email} for request {service_request.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {str(e)}")
        return False

def send_new_request_notification_email(service_request):
    """Send notification email to company about new service request"""
    try:
        company = service_request.service.company
        customer = service_request.customer
        service = service_request.service
        
        context = {
            'company_name': company.username,
            'service_name': service.name,
            'customer_name': customer.username,
            'customer_email': customer.email,
            'address': service_request.address,
            'service_hours': service_request.service_time_hours,
            'calculated_cost': service_request.calculated_cost,
            'date_requested': service_request.date_requested.strftime('%B %d, %Y at %I:%M %p'),
            'requests_url': f"{settings.SITE_URL}/services/requests/" if hasattr(settings, 'SITE_URL') else '#'
        }
        
        html_message = render_to_string('services/emails/new_request_notification.html', context)
        
        # Use SendGrid Web API in production, SMTP in development
        if not settings.DEBUG and hasattr(settings, 'SENDGRID_API_KEY') and settings.SENDGRID_API_KEY:
            return send_sendgrid_email(
                to_email=company.email,
                subject=f'New Service Request - {service.name}',
                html_content=html_message
            )
        else:
            send_mail(
                subject=f'New Service Request - {service.name}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[company.email],
                html_message=html_message,
                fail_silently=True,
            )
        
        logger.info(f"Notification email sent to {company.email} for request {service_request.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send notification email: {str(e)}")
        return False

def send_sendgrid_email(to_email, subject, html_content):
    """Send email using SendGrid Web API"""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        
        logger.info(f"SendGrid email sent successfully. Status: {response.status_code}")
        return True
        
    except Exception as e:
        logger.error(f"SendGrid email failed: {str(e)}")
        return False
