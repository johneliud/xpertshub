from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user_type = request.session.get('user_type', 'customer')
        
        # Set user type
        user.user_type = user_type
        
        # Set email and names from Google
        if sociallogin.account.extra_data:
            email = sociallogin.account.extra_data.get('email')
            name = sociallogin.account.extra_data.get('name', '')
            
            if email:
                user.email = email
            
            if name:
                name_parts = name.split(' ', 1)
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]
                else:
                    user.last_name = ''
                
                # Generate username from first and last name
                base_username = f"{user.first_name.lower()}.{user.last_name.lower()}" if user.last_name else user.first_name.lower()
                
                # Ensure unique username
                from .models import User
                username = base_username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user.username = username
        
        user.save()
        return user
