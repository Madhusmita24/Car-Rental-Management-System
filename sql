CREATE DATABASE car_rental;

USE car_rental;

CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(50),
    rent_per_day FLOAT,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT,
    customer_name VARCHAR(100),
    days INT,
    total_cost FLOAT,
    FOREIGN KEY (car_id) REFERENCES cars(id)
);