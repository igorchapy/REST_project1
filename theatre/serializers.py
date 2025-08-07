from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    TheatreHall, Play, Performance, Reservation,
    Ticket, Genre, Actor
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row"]


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]
        read_only_fields = ["reservation"]


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["row", "seat", "performance"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "tickets"]

    def validate(self, attrs):
        """Ensure no double-booked tickets."""
        performance = attrs["tickets"][0]["performance"]
        ticket_data = attrs["tickets"]

        # Collect all requested seats
        requested = {(t["row"], t["seat"]) for t in ticket_data}

        # Get already booked tickets for that performance
        existing = Ticket.objects.filter(
            performance=performance,
            row__in=[t["row"] for t in ticket_data],
            seat__in=[t["seat"] for t in ticket_data]
        ).values_list("row", "seat")

        existing_set = set(existing)

        duplicates = requested & existing_set
        if duplicates:
            raise ValidationError(f"Seats already taken: {duplicates}")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        reservation = Reservation.objects.create(**validated_data)
        Ticket.objects.bulk_create([
            Ticket(reservation=reservation, **ticket) for ticket in tickets_data
        ])
        return reservation
