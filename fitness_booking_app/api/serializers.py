from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone
import pytz


class FitnessClassSerializer(serializers.ModelSerializer):
    # Display the date/time in requested timezone (if passed in context)
    localized_date_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'date_time', 'available_slots', 'localized_date_time']

    def get_localized_date_time(self, obj):
        request = self.context.get('request')
        tz_name = request.query_params.get('timezone') if request else None
        try:
            tz = pytz.timezone(tz_name) if tz_name else timezone.get_current_timezone()
        except pytz.UnknownTimeZoneError:
            tz = timezone.get_current_timezone()
        return obj.date_time.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email']

    def validate(self, data):
        fitness_class = data.get('fitness_class')

        if fitness_class.available_slots < 1:
            raise serializers.ValidationError("No slots available for this class.")

        return data

    def create(self, validated_data):
        # Decrease available slots
        fitness_class = validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()

        return super().create(validated_data)
