from django.shortcuts import render

# Create your views here.
import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

# Configure logger
logger = logging.getLogger(__name__)

class FitnessClassListView(generics.ListAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_serializer_context(self):
        logger.info("Fetching serializer context for FitnessClassListView.")
        return {"request": self.request}


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new booking.")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Booking created successfully: {response.data}")
        return response


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if not email:
            logger.error("Email query param is missing.")
            raise ValidationError({"error": "Email query param is required."})
        logger.info(f"Fetching bookings for email: {email}")
        return Booking.objects.filter(client_email=email)