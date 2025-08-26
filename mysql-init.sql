-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS travel_booking CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'travel_user' @ '%' IDENTIFIED BY 'travel_password';

GRANT ALL PRIVILEGES ON travel_booking.* TO 'travel_user' @ '%';

FLUSH PRIVILEGES;
