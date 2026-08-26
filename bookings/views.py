from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from vendors.models import VendorProfile
from .forms import BookingForm, ConversationMessageForm
from .models import Booking
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


@login_required
def create_booking(request, vendor_pk):
    vendor = get_object_or_404(VendorProfile, pk=vendor_pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.vendor = vendor
            booking.status = 'requested'
            booking.save()
            # notify vendor (console email backend will print)
            send_mail(
                subject=f'New booking request for {vendor.business_name}',
                message=(
                    f'New booking request #{booking.pk}\n\n'
                    f'Client: {booking.full_name}\n'
                    f'Email: {booking.email}\n'
                    f'Phone: {booking.phone or "Not provided"}\n'
                    f'Event: {booking.event_type}\n'
                    f'Date: {booking.event_date or "To be confirmed"}\n'
                    f'Guests: {booking.guests or "To be confirmed"}\n\n'
                    f'Message:\n{booking.message or "No message provided."}\n\n'
                    'Log in to BM Events to respond.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[vendor.user.email] if vendor.user.email else [],
                fail_silently=False,
            )
            messages.success(request, 'Booking request submitted.')
            return redirect('client_activities')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'full_name': request.user.get_full_name() or request.user.username, 'email': request.user.email}
        form = BookingForm(initial=initial)
    return render(request, 'bookings/create_booking.html', {'form': form, 'vendor': vendor})


@login_required
def client_activities(request):
    bookings = request.user.bookings.select_related('vendor').order_by('-created_at')
    return render(request, 'bookings/client_activities.html', {'bookings': bookings})


@login_required
def booking_conversation(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('vendor__user', 'client'), pk=pk)
    if request.user != booking.client and request.user != booking.vendor.user:
        messages.error(request, 'You are not authorized to view this conversation.')
        return redirect('index')
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.booking = booking
            message.sender = request.user
            message.save()
            return redirect('booking_conversation', pk=booking.pk)
    else:
        form = ConversationMessageForm()
    conversation = booking.conversation_messages.select_related('sender').all()
    return render(request, 'bookings/conversation.html', {'booking': booking, 'conversation': conversation, 'form': form})


@login_required
def vendor_requests(request):
    # vendor's incoming bookings
    user = request.user
    if not user.is_vendor():
        return redirect('index')
    vendor = get_object_or_404(VendorProfile, user=user)
    bookings = vendor.bookings.order_by('-created_at')
    return render(request, 'bookings/vendor_requests.html', {'bookings': bookings, 'vendor': vendor})


@login_required
def booking_accept(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    user = request.user
    if not user.is_vendor() or booking.vendor.user != user:
        messages.error(request, 'Not authorized')
        return redirect('index')
    booking.status = 'accepted'
    booking.save()
    # notify client
    if booking.email:
        send_mail(
            subject=f'Your booking #{booking.pk} was accepted',
            message=f'Your booking for {booking.vendor.business_name} has been accepted. Please proceed to payment.',
            from_email=None,
            recipient_list=[booking.email],
        )
    messages.success(request, 'Booking accepted.')
    return redirect('vendor_requests')


@login_required
def booking_decline(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    user = request.user
    if not user.is_vendor() or booking.vendor.user != user:
        messages.error(request, 'Not authorized')
        return redirect('index')
    booking.status = 'declined'
    booking.save()
    if booking.email:
        send_mail(
            subject=f'Your booking #{booking.pk} was declined',
            message=f'Sorry, your booking for {booking.vendor.business_name} was declined.',
            from_email=None,
            recipient_list=[booking.email],
        )
    messages.success(request, 'Booking declined.')
    return redirect('vendor_requests')


@login_required
def booking_payment(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.client != request.user:
        messages.error(request, 'Not authorized')
        return redirect('index')
    if booking.status != 'accepted':
        messages.error(request, 'Booking not accepted yet')
        return redirect('index')
    if request.method == 'POST':
        # placeholder: mark as paid
        booking.status = 'paid'
        booking.save()
        messages.success(request, 'Payment recorded (placeholder).')
        return redirect('booking_detail', pk=booking.pk)
    return render(request, 'bookings/payment.html', {'booking': booking})


def booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('vendor__user', 'client'), pk=pk)
    if not request.user.is_authenticated or (request.user != booking.client and request.user != booking.vendor.user):
        messages.error(request, 'You are not authorized to view this booking.')
        return redirect('login')
    return render(request, 'bookings/booking_detail.html', {'booking': booking})
