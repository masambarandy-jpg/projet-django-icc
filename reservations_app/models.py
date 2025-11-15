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

    commentaire = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-date_reservation", "-heure_reservation", "-created_at"]

    def __str__(self):
        return f"{self.nom_client} – {self.date_reservation} {self.heure_reservation} ({self.nombre_personnes}p)"


