from django.urls import path
from . import views

urlpatterns = [
    path("", views.reservation_list, name="reservation_list"),
    path("reservations/nouvelle/", views.reservation_create, name="reservation_create"),
    path("reservations/<int:pk>/modifier/", views.reservation_update, name="reservation_update"),
    path("reservations/<int:pk>/supprimer/", views.reservation_delete, name="reservation_delete"),
    path("reservations/<int:pk>/modifier/", views.reservation_update, name="reservation_update"),
path("reservations/<int:pk>/supprimer/", views.reservation_delete, name="reservation_delete"),

]

