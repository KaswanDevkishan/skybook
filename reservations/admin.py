from django.contrib import admin

from reservations.models import Airline, Booking, City, Flight, Seat

admin.site.register([City, Airline, Flight, Seat, Booking])
