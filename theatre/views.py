from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import (
    Genre, Actor, TheatreHall, Play,
    Performance, Reservation, Ticket
)

from .serializers import (
    GenreSerializer, ActorSerializer, TheatreHallSerializer,
    PlaySerializer, PlayDetailSerializer, PerformanceSerializer,
    ReservationSerializer, TicketSerializer
)


class IsAdminOrIfAuthenticatedReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

class ActorViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        genre_ids = self.request.query_params.get("genres")
        actor_ids = self.request.query_params.get("actors")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre_ids:
            ids = [int(i) for i in genre_ids.split(",")]
            queryset = queryset.filter(genres__id__in=ids)
        if actor_ids:
            ids = [int(i) for i in actor_ids.split(",")]
            queryset = queryset.filter(actors__id__in=ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter("genres", type={"type": "list", "items": {"type": "number"}}, description="Filter by genre ids"),
            OpenApiParameter("actors", type={"type": "list", "items": {"type": "number"}}, description="Filter by actor ids"),
            OpenApiParameter("title", OpenApiTypes.STR, description="Filter by title"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get("date")
        play_id = self.request.query_params.get("play")

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(show_time__date=date)
            except ValueError:
                pass

        if play_id:
            queryset = queryset.filter(play_id=play_id)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter("play", OpenApiTypes.INT, description="Filter by play ID"),
            OpenApiParameter("date", OpenApiTypes.DATE, description="Filter by date (YYYY-MM-DD)"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ticket.objects.select_related("performance", "reservation")
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser,)
