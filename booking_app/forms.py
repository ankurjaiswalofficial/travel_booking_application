from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Booking
from django.utils import timezone


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    password = None  # Remove password field

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TravelSearchForm(forms.Form):
    TRAVEL_TYPES = [
        ('', 'All Types'),
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    travel_type = forms.ChoiceField(choices=TRAVEL_TYPES, required=False)
    source = forms.CharField(max_length=100, required=False)
    destination = forms.CharField(max_length=100, required=False)
    departure_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_departure_date(self):
        date = self.cleaned_data.get('departure_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError(
                "Departure date cannot be in the past.")
        return date


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        widgets = {
            'number_of_seats': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)

    def clean_number_of_seats(self):
        number_of_seats = self.cleaned_data.get('number_of_seats')
        if number_of_seats <= 0:
            raise forms.ValidationError("Number of seats must be at least 1.")

        if self.travel_option and not self.travel_option.is_available(number_of_seats):
            raise forms.ValidationError(
                f"Only {self.travel_option.available_seats} seats available.")

        return number_of_seats
