from django.db import models
from django.utils import timezone
from datetime import date, time


class Reservation(models.Model):
    nom_client = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    date_reservation = models.DateField(default=date.today)
    heure_reservation = models.TimeField(default=time(19, 0))  # 19:00 par défaut
    nombre_personnes = models.PositiveIntegerField(default=1)
    
    table = models.ForeignKey(
        "Table",  # on référence le modèle Table par son nom
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reservations",
        verbose_name="Table (optionnel)",
    )


    commentaire = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-date_reservation", "-heure_reservation", "-created_at"]

    def __str__(self):
        return f"{self.nom_client} – {self.date_reservation} {self.heure_reservation} ({self.nombre_personnes}p)"

class Table(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    capacite = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Table {self.numero} ({self.capacite} pers.)"

class OpeningHour(models.Model):
    # 0 = lundi, 6 = dimanche
    JOUR_SEMAINE = [
        (0, "Lundi"),
        (1, "Mardi"),
        (2, "Mercredi"),
        (3, "Jeudi"),
        (4, "Vendredi"),
        (5, "Samedi"),
        (6, "Dimanche"),
    ]

    jour = models.IntegerField(choices=JOUR_SEMAINE)
    heure_ouverture = models.TimeField()
    heure_fermeture = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["jour", "heure_ouverture"]
        verbose_name = "Horaire d'ouverture"
        verbose_name_plural = "Horaires d'ouverture"

    def __str__(self):
        if self.is_closed:
            return f"{self.get_jour_display()} : fermé"
        return f"{self.get_jour_display()} : {self.heure_ouverture.strftime('%H:%M')} → {self.heure_fermeture.strftime('%H:%M')}"
class SpecialDay(models.Model):
    date = models.DateField(unique=True)
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ex : Jour férié, fermeture exceptionnelle, événement spécial…",
    )
    is_closed = models.BooleanField(
        default=False,
        help_text="Cochez si le salon est complètement fermé ce jour-là.",
    )
    heure_ouverture = models.TimeField(
        null=True,
        blank=True,
        help_text="Laisser vide si fermé toute la journée.",
    )
    heure_fermeture = models.TimeField(
        null=True,
        blank=True,
        help_text="Laisser vide si fermé toute la journée.",
    )

    class Meta:
        ordering = ["date"]
        verbose_name = "Jour spécial"
        verbose_name_plural = "Jours spéciaux"

    def __str__(self):
        base = self.label or self.date.strftime("%d/%m/%Y")
        if self.is_closed:
            return f"{base} (fermé)"
        if self.heure_ouverture and self.heure_fermeture:
            return f"{base} ({self.heure_ouverture.strftime('%H:%M')} → {self.heure_fermeture.strftime('%H:%M')})"
        return base
