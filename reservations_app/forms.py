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
        table = cleaned_data.get("table")  # peut être None si tu la laisses optionnelle

        # Si un des champs est manquant, on laisse les autres validations gérer
        if not date_reservation or not heure_reservation:
            return cleaned_data

        # 1️⃣ Vérification des horaires d’ouverture (ce que tu avais déjà)
        if not is_time_within_opening(date_reservation, heure_reservation):
            raise ValidationError(
                "Ce créneau n'est pas disponible : le salon est fermé ou hors horaires d'ouverture."
            )

        # 2️⃣ Vérification des doublons de réservation
        from .models import Reservation  # déjà importé en haut, mais au cas où

        # On cherche les réservations qui ont :
        # - même date
        # - même heure
        # - même table (ou aucune table si table est vide)
        qs = Reservation.objects.filter(
            date_reservation=date_reservation,
            heure_reservation=heure_reservation,
        )

        if table:
            qs = qs.filter(table=table)
        else:
            qs = qs.filter(table__isnull=True)

        # Si on est en modification, on exclut la réservation actuelle
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            # Conflit détecté
            raise ValidationError(
                "Ce créneau est déjà réservé pour cette table. "
                "Choisissez une autre table ou un autre horaire."
            )

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()

        date_reservation = cleaned_data.get("date_reservation")
        heure_reservation = cleaned_data.get("heure_reservation")
        table = cleaned_data.get("table")
        nombre_personnes = cleaned_data.get("nombre_personnes")

        # ⬇️ 1. Si date ou heure manquent : on laisse les autres validations gérer
        if not date_reservation or not heure_reservation:
            return cleaned_data

        # 🔹 2. Vérification des horaires d'ouverture (déjà en place normalement)
        # ... ton code actuel pour is_time_within_opening / jours spéciaux ...

        # 🔹 3. Vérification des doublons (même table, même date, même heure)
        # ... ton code actuel qui vérifie les réservations existantes ...

        # 🔹 4. Vérification de la capacité de la table
        if table and nombre_personnes:
            if nombre_personnes > table.capacite:
                # On attache l'erreur spécifiquement au champ "nombre_personnes"
                raise ValidationError({
                    "nombre_personnes": (
                        f"Cette table ne peut accueillir que "
                        f"{table.capacite} personnes au maximum."
                    )
                })

        return cleaned_data

