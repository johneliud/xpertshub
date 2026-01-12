from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user_type = request.session.get('user_type', 'customer')
        
        # Set user type
        user.user_type = user_type
        
        # Set email and username from Google
        if sociallogin.account.extra_data:
            email = sociallogin.account.extra_data.get('email')
            name = sociallogin.account.extra_data.get('name', '')
            
            if email:
                user.email = email
                user.username = email  # Use email as username
            
            if name:
                # Split name into first and last name
                name_parts = name.split(' ', 1)
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]
        
        user.save()
        return user
    
    def get_login_redirect_url(self, request):
        user = request.user
        
        # Check if user needs to complete profile
        if hasattr(user, 'user_type'):
            if user.user_type == 'customer' and not user.date_of_birth:
                return reverse('complete_customer_profile')
            elif user.user_type == 'company' and not user.field_of_work:
                return reverse('complete_company_profile')
        
        return '/'
