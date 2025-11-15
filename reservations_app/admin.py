from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("nom_client", "date_reservation", "heure_reservation", "nombre_personnes", "created_at")
    list_filter = ("date_reservation", "heure_reservation")
    search_fields = ("nom_client", "email", "telephone")

