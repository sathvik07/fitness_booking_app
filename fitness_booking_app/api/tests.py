from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FitnessClass, Booking
from django.utils import timezone
import pytz

class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.fitness_class = FitnessClass.objects.create(
            name="Test Yoga",
            instructor="Test Instructor",
            date_time=timezone.now(),
            available_slots=1
        )

    def test_get_classes_with_timezone(self):
        url = reverse('class-list') + '?timezone=Asia/Kolkata'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('localized_date_time', response.data[0])

    def test_successful_booking(self):
        url = reverse('book-class')
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 0)

    def test_overbooking_prevention(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Bob",
            client_email="bob@example.com"
        )
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        url = reverse('book-class')
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Charlie",
            "client_email": "charlie@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Alice",
            client_email="alice@example.com"
        )
        url = reverse('booking-list') + '?email=alice@example.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
