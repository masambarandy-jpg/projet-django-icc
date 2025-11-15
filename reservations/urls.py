from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reservations_app.urls")),  # 👈 cette ligne relie ton app principale
]

