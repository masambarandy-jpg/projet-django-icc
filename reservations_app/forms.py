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
