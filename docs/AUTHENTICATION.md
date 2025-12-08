# Authentication System

This document explains how authentication is implemented in XpertsHub, including user registration, login, logout, and profile management.

## Overview

XpertsHub uses Django's built-in authentication system with custom extensions to support two user types (customers and companies) and email-based login.

## User Model

### Custom User Model
- Extends Django's `AbstractUser`
- Located in `users/models.py`
- Supports two user types: `customer` and `company`

### User Fields
```python
class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)  # For customers
    field_of_work = models.CharField(max_length=50, choices=FIELD_OF_WORK_CHOICES, null=True, blank=True)  # For companies
```

## Authentication Backend

### Email Authentication
- Custom authentication backend in `users/backends.py`
- Allows users to login with email instead of username
- Falls back to Django's default username authentication

```python
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
```

### Configuration
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

## Registration System

### Customer Registration
- Form: `CustomerRegistrationForm` in `users/forms.py`
- View: `CustomerRegisterView` in `users/views.py`
- Template: `users/customer_register.html`
- URL: `/auth/register/customer/`

### Company Registration
- Form: `CompanyRegistrationForm` in `users/forms.py`
- View: `CompanyRegisterView` in `users/views.py`
- Template: `users/company_register.html`
- URL: `/auth/register/company/`

### Registration Process
1. User fills out registration form
2. Form validates password confirmation
3. User type is automatically set based on registration type
4. Password is hashed using `set_password()`
5. User is saved to database
6. User is redirected to login page

## Login System

### Login Form
- Custom form extending Django's `AuthenticationForm`
- Uses email field instead of username
- Located in `users/forms.py`

### Login Process
1. User enters email and password
2. Custom `EmailBackend` authenticates user
3. Session is created
4. User is redirected to homepage

### Login Configuration
```python
# settings.py
LOGIN_REDIRECT_URL = '/'
```

## Logout System

### Logout Implementation
- Custom `UserLogoutView` in `xpertshub_app/views.py`
- Supports both GET and POST requests
- Immediately logs out user and redirects to homepage

```python
class UserLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
```

### Logout Configuration
```python
# settings.py
LOGOUT_REDIRECT_URL = '/'
```

## Profile System

### Profile Views
- Single `ProfileView` handles both customer and company profiles
- Uses dynamic template selection based on user type
- URL pattern: `/auth/profile/<username>/`

### Template Selection
```python
def get_template_names(self):
    if self.object.user_type == 'customer':
        return ['users/customer_profile.html']
    else:
        return ['users/company_profile.html']
```

## Security Features

### Password Security
- Uses Django's built-in password hashing
- Password confirmation validation in forms
- Passwords are never stored in plain text

### Form Security
- CSRF protection on all forms
- Form validation and error handling
- Unique email and username validation

### Session Security
- Django's default session management
- Secure logout functionality
- Proper session cleanup

## URL Configuration

### Authentication URLs
```python
# users/urls.py
urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/company/', CompanyRegisterView.as_view(), name='company_register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]
```

### Main URL Integration
```python
# xpertshub/urls.py
urlpatterns = [
    path('auth/', include('users.urls')),
]
```

## Frontend Integration

### Navigation
- Dynamic navigation based on authentication status
- Profile link for authenticated users
- Login/Register links for anonymous users

### Form Styling
- Tailwind CSS styling for all forms
- Responsive design
- Password visibility toggle functionality

### Template Inheritance
- All authentication templates extend `xpertshub_app/base.html`
- Consistent styling and navigation
- Reusable components for profile pages

## Error Handling

### Form Validation
- Password confirmation matching
- Unique email/username validation
- Field-specific error messages

### Authentication Errors
- Invalid login credentials
- Account not found
- Session expiration handling

## Testing Authentication

### Manual Testing
1. Register as customer and company
2. Login with email and password
3. Access profile pages
4. Test logout functionality
5. Verify session management

### Database Verification
- Check user creation in admin panel
- Verify password hashing
- Confirm user type assignment
