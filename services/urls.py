from django.urls import path
from .views import CreateServiceView, AllServicesView

urlpatterns = [
    path('', AllServicesView.as_view(), name='all_services'),
    path('create/', CreateServiceView.as_view(), name='create_service'),
]
