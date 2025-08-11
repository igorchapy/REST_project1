from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    TheatreHallViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TicketViewSet,
)


router = DefaultRouter()
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"theatre-halls", TheatreHallViewSet)
router.register(r"plays", PlayViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"reservations", ReservationViewSet, basename="reservations")
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "theatre"
