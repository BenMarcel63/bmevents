from django.contrib.auth import get_user_model
from vendors.models import VendorProfile
from bookings.models import Booking

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print('created admin')
else:
    print('admin exists')

if not User.objects.filter(username='vendor1').exists():
    v = User.objects.create_user('vendor1', 'vendor1@example.com', 'vendorpass')
    v.role = 'vendor'
    v.save()
    vp = VendorProfile.objects.create(user=v, business_name='Sample Vendor', description='Sample vendor created for testing')
    print('created vendor1')
else:
    vp = VendorProfile.objects.first()
    print('vendor1 exists')

if not User.objects.filter(username='client1').exists():
    c = User.objects.create_user('client1', 'client1@example.com', 'clientpass')
    c.role = 'client'
    c.save()
    print('created client1')
else:
    c = User.objects.get(username='client1')
    print('client1 exists')

# create a sample booking
bk = Booking.objects.create(client=c, vendor=vp, full_name='Client One', email=c.email, event_type='Wedding')
print('created booking', bk.pk)
