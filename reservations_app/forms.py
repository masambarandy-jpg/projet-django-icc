from .utils import is_time_within_opening
from django.core.exceptions import ValidationError

from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "nom_client",
            "email",
            "telephone",
            "date_reservation",
            "heure_reservation",
            "nombre_personnes",
        ]

        labels = {
            "nom_client": "Nom du client",
            "email": "Adresse e-mail",
            "telephone": "Téléphone",
            "date_reservation": "Date de la réservation",
            "heure_reservation": "Heure de la réservation",
            "nombre_personnes": "Nombre de personnes",
        }

        widgets = {
            "nom_client": forms.TextInput(
                attrs={
                    "placeholder": "Ex : Randy Masamba",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ex : randy@example.com",
                }
            ),
            "telephone": forms.TextInput(
                attrs={
                    "placeholder": "Ex : 0470 12 34 56",
                }
            ),
            "date_reservation": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "heure_reservation": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),
            "nombre_personnes": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),
        }
from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation
from .utils import is_time_within_opening


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        date_reservation = cleaned_data.get("date_reservation")
        heure_reservation = cleaned_data.get("heure_reservation")

        # Si un des deux est manquant, laisser les autres validations s’occuper
        if not date_reservation or not heure_reservation:
            return cleaned_data

        # Utiliser ta fonction utilitaire
        if not is_time_within_opening(date_reservation, heure_reservation):
            raise ValidationError(
                "Ce créneau n'est pas disponible : le salon est fermé ou hors horaires d'ouverture."
            )

        return cleaned_data
