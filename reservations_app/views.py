from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Reservation
from .forms import ReservationForm

# … tes autres imports

def reservation_list(request):
    q = (request.GET.get("q") or "").strip()
    sort = request.GET.get("sort", "date")
    dir_ = request.GET.get("dir", "asc")  # éviter d'ombrer la fonction built-in dir()

    # Base de la requête
    reservations = Reservation.objects.all()

    # Recherche texte
    if q:
        reservations = reservations.filter(
            Q(nom_client__icontains=q)
            | Q(telephone__icontains=q)
            | Q(date_reservation__icontains=q)
            | Q(heure_reservation__icontains=q)
        )

    # Filtres avancés
    date_start = request.GET.get("date_start") or ""
    date_end   = request.GET.get("date_end") or ""
    min_p      = request.GET.get("min_p") or ""
    max_p      = request.GET.get("max_p") or ""

    if date_start:
        reservations = reservations.filter(date_reservation__gte=date_start)
    if date_end:
        reservations = reservations.filter(date_reservation__lte=date_end)
    if min_p.isdigit():
        reservations = reservations.filter(nombre_personnes__gte=int(min_p))
    if max_p.isdigit():
        reservations = reservations.filter(nombre_personnes__lte=int(max_p))

    # Tri
    sort_map = {
        "date": "date_reservation",
        "heure": "heure_reservation",
        "client": "nom_client",
        "personnes": "nombre_personnes",
        "tel": "telephone",
    }
    sort_field = sort_map.get(sort, "date_reservation")
    if dir_ == "desc":
        sort_field = f"-{sort_field}"
    reservations = reservations.order_by(sort_field, "-id")

    # Pagination
    paginator = Paginator(reservations, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Rendu
    return render(
        request,
        "reservations_app/reservation_list.html",
        {
            "page_obj": page_obj,
            "q": q,
            "sort": sort,
            "dir": dir_,
            "date_start": date_start,
            "date_end": date_end,
            "min_p": min_p,
            "max_p": max_p,
        },
    )

def reservation_create(request):
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation créée avec succès.")  # tu peux remettre l'emoji si tu veux
            # Redirige vers next si présent
            return redirect(next_url or "reservation_list")
    else:
        form = ReservationForm()

    return render(
        request,
        "reservations_app/reservation_form.html",
        {"form": form, "mode": "create", "next": next_url},
    )


def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation modifiée avec succès.")
            return redirect(next_url or "reservation_list")
    else:
        form = ReservationForm(instance=reservation)

    return render(
        request,
        "reservations_app/reservation_form.html",
        {"form": form, "mode": "update", "next": next_url},
    )


def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Réservation supprimée avec succès.")
        return redirect(next_url or "reservation_list")

    return render(
        request,
        "reservations_app/confirm_delete.html",
        {"reservation": reservation, "next": next_url},
    )
from django.urls import reverse
from urllib.parse import urlencode

def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    params = {
        "q": request.GET.get("q", ""),
        "date_start": request.GET.get("date_start", ""),
        "date_end": request.GET.get("date_end", ""),
        "min_p": request.GET.get("min_p", ""),
        "max_p": request.GET.get("max_p", ""),
        "sort": request.GET.get("sort", ""),
        "dir": request.GET.get("dir", ""),
    }

    params = {k: v for k, v in params.items() if v}

    base_url = reverse("reservation_list")
    next_url = f"{base_url}?{urlencode(params)}" if params else base_url

    return render(request, 'reservations_app/reservation_detail.html', {
        "reservation": reservation,
        "next_url": next_url,
    })

