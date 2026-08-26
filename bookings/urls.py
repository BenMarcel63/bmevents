from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.client_activities, name='client_activities'),
    path('vendor/<int:vendor_pk>/book/', views.create_booking, name='create_booking'),
    path('booking/<int:pk>/conversation/', views.booking_conversation, name='booking_conversation'),
    path('vendor/requests/', views.vendor_requests, name='vendor_requests'),
    path('booking/<int:pk>/accept/', views.booking_accept, name='booking_accept'),
    path('booking/<int:pk>/decline/', views.booking_decline, name='booking_decline'),
    path('booking/<int:pk>/payment/', views.booking_payment, name='booking_payment'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
]
