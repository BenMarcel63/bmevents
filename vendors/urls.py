from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('edit/', views.edit_vendor_profile, name='edit_vendor_profile'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('service/add/', views.add_service, name='add_service'),
    path('service/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('gallery/add/', views.add_gallery_image, name='add_gallery_image'),
]
