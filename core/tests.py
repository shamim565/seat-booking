import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Venue, Seat, Booking

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def venue():
    return Venue.objects.create(name="Test Venue", location="Test Location", capacity=5)

@pytest.fixture
def seat(venue):
    return Seat.objects.create(venue=venue, seat_number="A1", type=0, price=50.0)

@pytest.fixture
def booking(seat):
    return Booking.objects.create(
        seat=seat,
        customer_name="Shamim Azad",
        phone="1234567890",
        email="shamim@example.com",
        event_date="2025-09-01",
        event_time="18:00:00",
    )
    

@pytest.mark.django_db
def test_create_venue(api_client):
    url = reverse('venues-list')
    data = {"name": "New Venue", "location": "New Location", "capacity": 200}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Venue.objects.count() == 1


@pytest.mark.django_db
def test_get_venues(api_client, venue):
    url = reverse('venues-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    

@pytest.mark.django_db
def test_venue_not_found(api_client):
    url = reverse('venues-detail', args=[9999])
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "No Venue matches the given query."


@pytest.mark.django_db
def test_retrieve_venue_by_id(api_client, venue):
    url = reverse('venues-detail', args=[venue.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == venue.name


@pytest.mark.django_db
def test_update_venue(api_client, venue):
    url = reverse('venues-detail', args=[venue.id])
    data = {"name": "Updated Venue", "location": venue.location, "capacity": venue.capacity}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    venue.refresh_from_db()
    assert venue.name == "Updated Venue"


@pytest.mark.django_db
def test_delete_venue(api_client, venue):
    url = reverse('venues-detail', args=[venue.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Venue.objects.count() == 0


@pytest.mark.django_db
def test_create_seat(api_client, venue):
    url = reverse('seats-list')
    data = {"venue": venue.id, "seat_number": "A2", "type": 0, "price": 50.0}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Seat.objects.count() == 1
    
    
@pytest.mark.django_db
def test_create_seat_exceeds_venue_capacity(api_client, venue):
    for i in range(venue.capacity):
        Seat.objects.create(venue=venue, seat_number=f"A{i+1}", type=0, price=50.0)
    
    url = reverse('seats-list')
    data = {"venue": venue.id, "seat_number": "A101", "type": 0, "price": 50.0}
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['venue'][0] == "Maximum venue capacity has exceeded."


@pytest.mark.django_db
def test_get_seats_list(api_client, seat):
    url = reverse('seats-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_seat_by_id(api_client, seat):
    url = reverse('seats-detail', args=[seat.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['seat_number'] == seat.seat_number
    

@pytest.mark.django_db
def test_seat_not_found(api_client):
    url = reverse('seats-detail', args=[9999])
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "No Seat matches the given query."


@pytest.mark.django_db
def test_update_seat(api_client, seat):
    url = reverse('seats-detail', args=[seat.id])
    data = {"venue": seat.venue.id, "seat_number": "A1", "type": 1, "price": 75.0}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    seat.refresh_from_db()
    assert seat.type == 1
    assert seat.price == 75.0


@pytest.mark.django_db
def test_delete_seat(api_client, seat):
    url = reverse('seats-detail', args=[seat.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Seat.objects.count() == 0


@pytest.mark.django_db
def test_create_booking(api_client, venue):
    url = reverse('bookings-list')
    seat = Seat.objects.create(venue=venue, seat_number="A2", type=0, price=50.0)
    data = {
        "seat": seat.id,
        "customer_name": "Shamim Azad",
        "phone": "1234567890",
        "email": "shamim@example.com",
        "event_date": "2025-09-01",
        "event_time": "18:00:00",
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.count() == 1
    seat.refresh_from_db()
    assert seat.is_booked is True
    

@pytest.mark.django_db
def test_create_booking_past_event_date(api_client, venue):
    url = reverse('bookings-list')
    seat = Seat.objects.create(venue=venue, seat_number="A2", type=0, price=50.0)
    data = {
        "seat": seat.id,
        "customer_name": "Shamim Azad",
        "phone": "1234567890",
        "email": "shamim@example.com",
        "event_date": "2023-01-01", 
        "event_time": "10:00:00",
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['event_time'][0] == "Event date and time must be in the future."
    
    
@pytest.mark.django_db
def test_create_booking_for_already_booked_seat(api_client, seat,  booking):
    url = reverse('bookings-list')
    data = {
        "seat": seat.id,
        "customer_name": "Shamim Azad",
        "phone": "1234567890",
        "email": "shamim@example.com",
        "event_date": "2025-09-01", 
        "event_time": "10:00:00",
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['seat'][0] == f"booking with this seat already exists."


@pytest.mark.django_db
def test_get_bookings_list(api_client, booking):
    url = reverse('bookings-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_booking_by_id(api_client, booking):
    url = reverse('bookings-detail', args=[booking.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['customer_name'] == booking.customer_name
    

@pytest.mark.django_db
def test_booking_not_found(api_client):
    url = reverse('bookings-detail', args=[9999])
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "No Booking matches the given query."


@pytest.mark.django_db
def test_delete_booking(api_client, seat, booking):
    url = reverse('bookings-detail', args=[booking.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Booking.objects.count() == 0
    seat.refresh_from_db()
    assert seat.is_booked is False
