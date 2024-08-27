from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, SeatViewSet, BookingViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'venues', VenueViewSet, basename='venues')
router.register(r'seats', SeatViewSet, basename='seats')
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
