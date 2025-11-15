from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Reservation
from .forms import ReservationForm


def reservation_list(request):
    q = (request.GET.get("q") or "").strip()

    qs = Reservation.objects.all().order_by(
        "-date_reservation", "-heure_reservation", "-created_at"
    )

    if q:
        qs = qs.filter(
            Q(nom_client__icontains=q)
            | Q(telephone__icontains=q)
            | Q(email__icontains=q)
            | Q(commentaire__icontains=q)
            | Q(date_reservation__icontains=q)
            | Q(heure_reservation__icontains=q)
        )

    paginator = Paginator(qs, 10)  # 10 lignes par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "reservations_app/reservation_list.html",
        {
            "page_obj": page_obj,
            "q": q,
        },
    )

def reservation_create(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation créée avec succès ✅")
            return redirect("reservation_list")
    else:
        form = ReservationForm()
    return render(
        request,
        "reservations_app/reservation_form.html",
        {"form": form, "mode": "create"},
    )


def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation mise à jour ✅")
            return redirect("reservation_list")
    else:
        form = ReservationForm(instance=reservation)
    return render(
        request,
        "reservations_app/reservation_form.html",
        {"form": form, "mode": "update"},
    )


def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Réservation supprimée ✅")
        return redirect("reservation_list")
    return render(
        request,
        "reservations_app/confirm_delete.html",
        {"reservation": reservation},
    )
