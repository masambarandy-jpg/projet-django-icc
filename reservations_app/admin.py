from django.contrib import admin
from .models import Reservation
from .models import Reservation, Table, OpeningHour
from .models import Reservation, Table, OpeningHour, SpecialDay



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
@admin.register(SpecialDay)
class SpecialDayAdmin(admin.ModelAdmin):
    list_display = ("date", "label", "is_closed", "heure_ouverture", "heure_fermeture")
    list_filter = ("is_closed",)
    search_fields = ("label",)

