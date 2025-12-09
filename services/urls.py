from django.urls import path
from .views import CreateServiceView

urlpatterns = [
    path('create/', CreateServiceView.as_view(), name='create_service'),
]
