from datetime import time
from typing import Optional, Tuple

from .models import OpeningHour, SpecialDay


def get_effective_opening_for_date(target_date) -> Tuple[bool, Optional[time], Optional[time]]:
    """
    Retourne un tuple (is_closed, open_time, close_time) pour un jour donné.

    - Si un SpecialDay existe pour cette date :
        - s'il est fermé -> (True, None, None)
        - sinon -> (False, heure_ouverture, heure_fermeture)
    - Sinon on regarde l'OpeningHour du jour de semaine :
        - si aucun horaire trouvé -> (True, None, None)
        - sinon -> (False, heure_ouverture, heure_fermeture)
    """
    # 1) On regarde d'abord s'il y a un jour spécial pour cette date
    special = SpecialDay.objects.filter(date=target_date).first()
    if special:
        if special.is_closed or not (special.heure_ouverture and special.heure_fermeture):
            return True, None, None
        return False, special.heure_ouverture, special.heure_fermeture

    # 2) Sinon, on regarde les horaires normaux pour ce jour de semaine
    weekday = target_date.weekday()  # 0=lundi, 6=dimanche
    oh = OpeningHour.objects.filter(jour=weekday, is_closed=False).first()

    if not oh:
        return True, None, None

    return False, oh.heure_ouverture, oh.heure_fermeture


def is_time_within_opening(target_date, target_time: time) -> bool:
    """
    True si la date/heure demandée tombe dans une plage d'ouverture effective.
    Prend en compte les jours spéciaux.
    """
    is_closed, open_t, close_t = get_effective_opening_for_date(target_date)
    if is_closed or not (open_t and close_t):
        return False

    return open_t <= target_time <= close_t
