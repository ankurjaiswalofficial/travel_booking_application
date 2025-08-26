from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    travel_id = models.CharField(max_length=50, unique=True)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_datetime']

    def __str__(self):
        return f"{self.travel_id} - {self.source} to {self.destination}"

    def is_available(self, seats_required=1):
        return self.available_seats >= seats_required


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(
        TravelOption, on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"BK{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def cancel(self):
        if self.status == 'confirmed':
            self.status = 'cancelled'
            self.travel_option.available_seats += self.number_of_seats
            self.travel_option.save()
            self.save()
            return True
        return False
