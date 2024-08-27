from rest_framework import serializers
from .models import Venue, Seat, Booking
from django.utils import timezone

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'location', 'capacity', 'created_at', 'updated_at']


class SeatSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)

    class Meta:
        model = Seat
        fields = ['id', 'venue', 'venue_name', 'seat_number', 'type', 'price', 'is_booked', 'created_at', 'updated_at']

    def validate(self, data):
        venue = data.get('venue')
        total_venue = Seat.objects.filter(venue=venue).count()
    
        if total_venue >= venue.capacity:
            raise serializers.ValidationError({"venue" : "Maximum venue capacity has exceeded."})
        
        return data
            


class BookingSerializer(serializers.ModelSerializer):
    seat_details = SeatSerializer(source='seat', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'seat', 'seat_details', 'customer_name', 'phone', 'email', 'event_date', 'event_time', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Custom validation logic for Booking to ensure event date/time is in the future
        and the seat is not already booked.
        """
        seat = data.get('seat')
        event_date = data.get('event_date')
        event_time = data.get('event_time')

        # Ensure event date and time are in the future
        if event_date < timezone.now().date() or (
            event_date == timezone.now().date() and event_time < timezone.now().time()
        ):
            raise serializers.ValidationError("Event date and time must be in the future.")

        # Ensure the seat isn't already booked
        if seat.is_booked:
            raise serializers.ValidationError(f"Seat {seat.seat_number} is already booked.")

        return data

    def create(self, validated_data):
        """
        Override the create method to mark the seat as booked when a new booking is created.
        """
        seat = validated_data['seat']
        seat.is_booked = True
        seat.save()
        return super().create(validated_data)
