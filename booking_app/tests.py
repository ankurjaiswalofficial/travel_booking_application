from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import BookingForm


class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.travel = TravelOption.objects.create(
            travel_id="FL123",
            travel_type="flight",
            source="New York",
            destination="London",
            departure_datetime=timezone.now() + timezone.timedelta(days=1),
            arrival_datetime=timezone.now() + timezone.timedelta(days=1, hours=8),
            price=500.00,
            available_seats=100
        )

    def test_travel_creation(self):
        self.assertEqual(self.travel.travel_id, "FL123")
        self.assertEqual(self.travel.available_seats, 100)

    def test_is_available(self):
        self.assertTrue(self.travel.is_available(50))
        self.assertFalse(self.travel.is_available(150))


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'password')
        self.travel = TravelOption.objects.create(
            travel_id="FL123",
            travel_type="flight",
            source="New York",
            destination="London",
            departure_datetime=timezone.now() + timezone.timedelta(days=1),
            arrival_datetime=timezone.now() + timezone.timedelta(days=1, hours=8),
            price=500.00,
            available_seats=100
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel,
            number_of_seats=2,
            total_price=1000.00
        )
        self.assertIsNotNone(booking.booking_id)
        self.assertEqual(booking.status, 'confirmed')


class BookingFormTest(TestCase):
    def setUp(self):
        self.travel = TravelOption.objects.create(
            travel_id="FL123",
            travel_type="flight",
            source="New York",
            destination="London",
            departure_datetime=timezone.now() + timezone.timedelta(days=1),
            arrival_datetime=timezone.now() + timezone.timedelta(days=1, hours=8),
            price=500.00,
            available_seats=10
        )

    def test_valid_booking(self):
        form = BookingForm({'number_of_seats': 2}, travel_option=self.travel)
        self.assertTrue(form.is_valid())

    def test_invalid_seats(self):
        form = BookingForm({'number_of_seats': 20}, travel_option=self.travel)
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'password')
        self.travel = TravelOption.objects.create(
            travel_id="FL123",
            travel_type="flight",
            source="New York",
            destination="London",
            departure_datetime=timezone.now() + timezone.timedelta(days=1),
            arrival_datetime=timezone.now() + timezone.timedelta(days=1, hours=8),
            price=500.00,
            available_seats=100
        )

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_travel_list_view(self):
        response = self.client.get('/travel/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.travel.source)
