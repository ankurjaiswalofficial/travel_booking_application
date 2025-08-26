import os
import django
import random
from datetime import timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from booking_app.models import TravelOption, Booking  # Replace with your app name

# India-specific cities and airports
INDIAN_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kochi', 'Goa',
    'Chandigarh', 'Bhopal', 'Indore', 'Nagpur', 'Surat', 'Varanasi',
    'Patna', 'Bhubaneswar', 'Thiruvananthapuram', 'Guwahati', 'Amritsar'
]

# Flight numbers and train numbers for different types
FLIGHT_PREFIXES = ['AI', '6E', 'SG', 'UK', 'G8', 'IX', 'QP']
TRAIN_NUMBERS = ['12301', '12259', '12260', '12951', '12952', '12953', '12954']
BUS_OPERATORS = ['RSRTC', 'UPSRTC', 'MSRTC', 'KSRTC', 'TSRTC', 'GSRTC']


def create_superuser():
    """Create a superuser if not exists"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin/admin123")


def generate_travel_id(travel_type):
    """Generate unique travel ID based on type"""
    if travel_type == 'flight':
        prefix = random.choice(FLIGHT_PREFIXES)
        return f"{prefix}{random.randint(100, 999)}"
    elif travel_type == 'train':
        return f"{random.choice(TRAIN_NUMBERS)}"
    else:  # bus
        operator = random.choice(BUS_OPERATORS)
        return f"{operator}-{random.randint(1000, 9999)}"


def generate_departure_arrival_times():
    """Generate realistic departure and arrival times"""
    departure = timezone.now() + timedelta(days=random.randint(1, 30))
    duration_hours = random.randint(1, 12)
    arrival = departure + timedelta(hours=duration_hours)
    return departure, arrival


def generate_price(travel_type, distance_factor):
    """Generate realistic prices based on travel type"""
    if travel_type == 'flight':
        base_price = 2000 + (distance_factor * 100)
    elif travel_type == 'train':
        base_price = 500 + (distance_factor * 50)
    else:  # bus
        base_price = 300 + (distance_factor * 30)

    # Add some random variation
    return round(base_price * random.uniform(0.9, 1.2), 2)


def create_travel_options(num_options=50):
    """Create travel options with India-specific data"""
    travel_options_created = 0

    for _ in range(num_options):
        travel_type = random.choice(['flight', 'train', 'bus'])
        source, destination = random.sample(INDIAN_CITIES, 2)

        # Ensure source and destination are different
        while source == destination:
            destination = random.choice(INDIAN_CITIES)

        # Generate travel ID and check if it already exists
        travel_id = generate_travel_id(travel_type)
        if TravelOption.objects.filter(travel_id=travel_id).exists():
            continue

        departure, arrival = generate_departure_arrival_times()

        # Calculate distance factor (simple heuristic based on city index difference)
        source_idx = INDIAN_CITIES.index(source)
        dest_idx = INDIAN_CITIES.index(destination)
        distance_factor = abs(source_idx - dest_idx) + 1

        price = generate_price(travel_type, distance_factor)
        available_seats = random.randint(10, 200)

        try:
            travel_option = TravelOption.objects.create(
                travel_id=travel_id,
                travel_type=travel_type,
                source=source,
                destination=destination,
                departure_datetime=departure,
                arrival_datetime=arrival,
                price=price,
                available_seats=available_seats
            )
            travel_options_created += 1
            print(
                f"Created {travel_type}: {source} to {destination} (₹{price})")

        except Exception as e:
            print(f"Error creating travel option: {e}")

    return travel_options_created


def create_sample_bookings(num_bookings=20):
    """Create sample bookings for demonstration"""
    bookings_created = 0
    travel_options = TravelOption.objects.all()
    users = User.objects.all()

    if not users.exists():
        # Create some test users
        test_users = [
            User.objects.create_user(
                'user1', 'user1@example.com', 'password123'),
            User.objects.create_user(
                'user2', 'user2@example.com', 'password123'),
            User.objects.create_user(
                'user3', 'user3@example.com', 'password123'),
        ]
        users = test_users

    for _ in range(num_bookings):
        travel_option = random.choice(travel_options)
        user = random.choice(users)
        number_of_seats = random.randint(
            1, min(5, travel_option.available_seats))

        # Skip if not enough seats
        if not travel_option.is_available(number_of_seats):
            continue

        total_price = travel_option.price * number_of_seats

        try:
            booking = Booking.objects.create(
                user=user,
                travel_option=travel_option,
                number_of_seats=number_of_seats,
                total_price=total_price
            )

            # Update available seats
            travel_option.available_seats -= number_of_seats
            travel_option.save()

            bookings_created += 1
            print(
                f"Created booking: {user.username} - {travel_option.travel_id} ({number_of_seats} seats)")

        except Exception as e:
            print(f"Error creating booking: {e}")

    return bookings_created


def clear_existing_data():
    """Clear existing data (optional - use with caution!)"""
    # Uncomment the lines below if you want to clear existing data
    # Booking.objects.all().delete()
    # TravelOption.objects.all().delete()
    # print("Cleared existing data")
    pass


def main():
    """Main function to populate the database"""
    print("Starting data population...")

    # Create superuser
    create_superuser()

    # Clear existing data (uncomment if needed)
    clear_existing_data()

    # Create travel options
    print("\nCreating travel options...")
    travel_options_count = create_travel_options(100)
    print(f"Created {travel_options_count} travel options")

    # Create sample bookings
    print("\nCreating sample bookings...")
    bookings_count = create_sample_bookings(30)
    print(f"Created {bookings_count} bookings")

    print("\nData population completed successfully!")
    print(f"Total Travel Options: {TravelOption.objects.count()}")
    print(f"Total Bookings: {Booking.objects.count()}")


if __name__ == "__main__":
    main()
