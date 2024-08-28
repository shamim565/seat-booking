from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Venue(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
    

class SeatType(models.IntegerChoices):
    REGULAR = 0, 'REGULAR'
    VIP = 1, 'VIP'

class Seat(BaseModel):
    venue = models.ForeignKey(Venue, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    type = models.PositiveBigIntegerField(choices=SeatType.choices, default=SeatType.REGULAR)
    price = models.FloatField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('venue', 'seat_number')

    def __str__(self):
        return f"Seat {self.seat_number} at {self.venue.name}"


class Booking(BaseModel):
    seat = models.OneToOneField(Seat, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()

    class Meta:
        unique_together = ('seat', 'event_date', 'event_time')

    def __str__(self):
        return f"Booking by {self.customer_name} for {self.seat}"

