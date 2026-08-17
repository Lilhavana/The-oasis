from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservationForm
from .models import Reservation, Table


def home(request):
    return render(request, 'bookings/home.html')


@login_required(login_url='login')
def make_reservation(request):
    tables = Table.objects.all().order_by('table_number')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            table = form.cleaned_data['table']
            conflict = Reservation.objects.filter(
                table=table,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            if conflict.exists():
                return render(request, 'bookings/make_reservation.html', {
                    'form': form, 'tables': tables,
                    'error': 'Sorry, that table is already booked for that time.',
                })
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('confirmation', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'bookings/make_reservation.html', {'form': form, 'tables': tables})


@login_required(login_url='login')
def my_reservations(request):
    date_filter = request.GET.get('date')
    reservations = Reservation.objects.all() if request.user.is_staff else Reservation.objects.filter(user=request.user)
    if date_filter:
        reservations = reservations.filter(date=date_filter)
    reservations = reservations.order_by('date', 'start_time')
    return render(request, 'bookings/my_reservations.html', {
        'reservations': reservations, 'date_filter': date_filter
    })


@login_required(login_url='login')
def confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not request.user.is_staff and reservation.user_id != request.user.id:
        return redirect('my_reservations')
    return render(request, 'bookings/confirmation.html', {'reservation': reservation})


@login_required(login_url='login')
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not request.user.is_staff and reservation.user_id != request.user.id:
        return redirect('my_reservations')
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'bookings/cancel_confirm.html', {'reservation': reservation})


def about(request):
    return render(request, 'bookings/about.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        if password != confirm:
            return render(request, 'bookings/signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'bookings/signup.html', {'error': 'Username already taken'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'bookings/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'bookings/login.html', {'error': 'Invalid username or password'})
    return render(request, 'bookings/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def menu(request):
    return render(request, 'bookings/menu.html')
