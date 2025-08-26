from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from booking_app.utils import paginate_objects
from .models import TravelOption, Booking
from .forms import UserRegistrationForm, UserProfileForm, TravelSearchForm, BookingForm


def home(request):
    travel_options = TravelOption.objects.filter(
        departure_datetime__gte=timezone.now(),
        available_seats__gt=0
    )[:6]
    return render(request, 'booking_app/home.html', {'travel_options': travel_options})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'booking_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'booking_app/profile.html', {'form': form})


def travel_list(request):
    form = TravelSearchForm(request.GET or None)
    travel_options = TravelOption.objects.filter(
        departure_datetime__gte=timezone.now(),
        available_seats__gt=0
    ).order_by('departure_datetime')

    if form.is_valid():
        travel_type = form.cleaned_data.get('travel_type')
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')

        if travel_type:
            travel_options = travel_options.filter(travel_type=travel_type)
        if source:
            travel_options = travel_options.filter(source__icontains=source)
        if destination:
            travel_options = travel_options.filter(
                destination__icontains=destination)
        if departure_date:
            travel_options = travel_options.filter(
                departure_datetime__date=departure_date)

    travel_options_page, paginator = paginate_objects(
        request, travel_options, 8)

    return render(request, 'booking_app/travel_list.html', {
        'travel_options': travel_options_page,
        'form': form,
        'paginator': paginator
    })


@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            number_of_seats = form.cleaned_data['number_of_seats']
            total_price = travel_option.price * number_of_seats

            booking = Booking(
                user=request.user,
                travel_option=travel_option,
                number_of_seats=number_of_seats,
                total_price=total_price
            )
            booking.save()

            # Update available seats
            travel_option.available_seats -= number_of_seats
            travel_option.save()

            messages.success(
                request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
            return redirect('booking_list')
    else:
        form = BookingForm(travel_option=travel_option)

    return render(request, 'booking_app/booking_form.html', {
        'form': form,
        'travel_option': travel_option
    })


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(
        user=request.user).order_by('-booking_date')

    bookings_page, paginator = paginate_objects(request, bookings, 8)

    return render(request, 'booking_app/booking_list.html', {
        'bookings': bookings_page,
        'paginator': paginator
    })


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking, booking_id=booking_id, user=request.user)
    return render(request, 'booking_app/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking, booking_id=booking_id, user=request.user)

    if booking.status == 'confirmed':
        if booking.cancel():
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'Unable to cancel booking.')
    else:
        messages.error(request, 'Booking is already cancelled.')

    return redirect('booking_list')
