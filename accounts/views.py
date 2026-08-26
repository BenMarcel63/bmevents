from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from vendors.models import VendorProfile


def index(request):
    # render the full design index template and pass vendors for the featured section
    from vendors.models import VendorProfile
    vendors = VendorProfile.objects.all()[:6]
    return render(request, 'index.html', {'vendors': vendors})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def register_vendor(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'vendor'
            user.save()
            # create empty VendorProfile for this user
            VendorProfile.objects.create(user=user, business_name=user.username)
            login(request, user)
            messages.success(request, 'Vendor account created. Please complete your vendor profile.')
            return redirect('edit_vendor_profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register_vendor.html', {'form': form})
