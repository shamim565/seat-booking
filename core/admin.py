from django.contrib import admin
from .models import Venue
from .models import Seat
from .models import Booking

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'location')

admin.site.register(Venue, VenueAdmin)


class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'venue', 'type', 'price', 'is_booked', 'created_at', 'updated_at')
    search_fields = ('seat_number', 'venue__name')
    ordering = ('venue', 'seat_number')

admin.site.register(Seat, SeatAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('seat', 'customer_name', 'phone', 'email', 'event_date', 'event_time', 'created_at')
    search_fields = ('customer_name', 'phone', 'email', 'seat__seat_number', 'seat__venue__name')
    ordering = ('-created_at',)

admin.site.register(Booking, BookingAdmin)

