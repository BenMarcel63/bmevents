from django.shortcuts import render, get_object_or_404, redirect
from .models import VendorProfile
from .forms import VendorProfileForm, ServiceForm, GalleryImageForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Service, GalleryImage



def vendor_list(request):
    vendors = VendorProfile.objects.all()
    return render(request, 'vendors/list.html', {'vendors': vendors})


def vendor_detail(request, pk):
    vendor = get_object_or_404(VendorProfile, pk=pk)
    return render(request, 'vendors/detail.html', {'vendor': vendor})


@login_required
def edit_vendor_profile(request):
    user = request.user
    try:
        profile = user.vendor_profile
    except VendorProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = VendorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('vendor_detail', pk=instance.pk)
    else:
        form = VendorProfileForm(instance=profile)

    return render(request, 'vendors/edit_profile.html', {'form': form})


@login_required
def vendor_dashboard(request):
    user = request.user
    if not getattr(user, 'is_vendor', False) and not user.is_vendor():
        return HttpResponseForbidden('Not a vendor')
    profile = get_object_or_404(VendorProfile, user=user)
    services = profile.services.all()
    gallery = profile.gallery.all()
    bookings = profile.bookings.select_related('client').order_by('-created_at')
    pending_requests = bookings.filter(status='requested').count()
    return render(request, 'vendors/dashboard.html', {'profile': profile, 'services': services, 'gallery': gallery, 'bookings': bookings, 'pending_requests': pending_requests})


@login_required
def add_service(request):
    user = request.user
    if not user.is_vendor():
        return HttpResponseForbidden('Not a vendor')
    profile = get_object_or_404(VendorProfile, user=user)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.vendor = profile
            service.save()
            return redirect('vendor_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'vendors/add_service.html', {'form': form})


@login_required
def edit_service(request, pk):
    user = request.user
    if not user.is_vendor():
        return HttpResponseForbidden('Not a vendor')
    service = get_object_or_404(Service, pk=pk)
    if service.vendor.user != user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'vendors/edit_service.html', {'form': form, 'service': service})


@login_required
def add_gallery_image(request):
    user = request.user
    if not user.is_vendor():
        return HttpResponseForbidden('Not a vendor')
    profile = get_object_or_404(VendorProfile, user=user)
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.vendor = profile
            img.save()
            return redirect('vendor_dashboard')
    else:
        form = GalleryImageForm()
    return render(request, 'vendors/add_image.html', {'form': form})
