from django.contrib import admin
from .models import Reservation
from .models import Reservation, Table, OpeningHour


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("nom_client", "date_reservation", "heure_reservation", "nombre_personnes", "created_at")
    list_filter = ("date_reservation", "heure_reservation")
    search_fields = ("nom_client", "email", "telephone")

from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("numero", "capacite")
    search_fields = ("numero",)
@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ("jour", "heure_ouverture", "heure_fermeture", "is_closed")
    list_filter = ("jour", "is_closed")
