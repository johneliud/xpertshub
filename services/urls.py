from django.urls import path
from .views import CreateServiceView, AllServicesView, ServicesByCategoryView, ServiceDetailView, RequestServiceView

urlpatterns = [
    path('', AllServicesView.as_view(), name='all_services'),
    path('create/', CreateServiceView.as_view(), name='create_service'),
    path('category/<str:field>/', ServicesByCategoryView.as_view(), name='services_by_category'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('<int:service_id>/request/', RequestServiceView.as_view(), name='request_service'),
]
