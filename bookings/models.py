from django.db import models
from django.conf import settings
from vendors.models import VendorProfile


class Booking(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='bookings')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField(null=True, blank=True)
    guests = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.pk} for {self.vendor.business_name} by {self.client.username}"


class ConversationMessage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='conversation_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_booking_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message for booking {self.booking_id} from {self.sender.username}'
