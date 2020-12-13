from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import BaseDetailView

from reservations.forms import (
    ReservationCreationForm,
    TurnsCreationForm,
    TurnsPreparationForm,
)
from reservations.models import Reservation
from reservations.turns import compute_turns
from rooms.models import Room


RESERVATION_CREATE_SUCCESS_MESSAGE = "Reserva registrada con éxito"
RESERVATION_EDIT_SUCCESS_MESSAGE = "Se guardaron los cambios sobre la reserva"
RESERVATION_DELETE_SUCCESS_MESSAGE = "Reserva eliminada"


class ReservationsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    http_method_names = ["get"]
    model = Reservation
    template_name = "reservations/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        def tuples_3(l):
            return (l[i : i + 3] for i in range(0, len(l), 3))

        context["next"] = tuples_3(Reservation.objects.filter(from_date__gte=today))
        context["past"] = tuples_3(Reservation.objects.filter(from_date__lt=today))
        context["rooms"] = Room.objects.all()
        return context


class ReservationCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = Reservation
    form_class = ReservationCreationForm
    # fields = ["from_date", "to_date", "rooms", "notes"]
    template_name = "reservations/create.html"
    success_url = reverse_lazy("reservations:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return RESERVATION_CREATE_SUCCESS_MESSAGE


class ReservationEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = Reservation
    form_class = ReservationCreationForm
    # fields = ["from_date", "to_date", "rooms", "notes"]
    template_name = "reservations/create.html"
    success_url = reverse_lazy("reservations:index")

    def form_valid(self, form):
        if not form.instance.user:
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return RESERVATION_EDIT_SUCCESS_MESSAGE


class ReservationDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Reservation
    success_url = reverse_lazy("reservations:index")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self):
        return RESERVATION_DELETE_SUCCESS_MESSAGE


class RoomReservations(LoginRequiredMixin, BaseDetailView):
    model = Room
    http_method_names = ["get"]
    pk_url_kwarg = "room_id"

    def get(self, request, room_id):
        room = self.get_object()
        params = self.request.GET
        reservations = room.filter_reservations_that_intersect(
            params["start"], params["end"]
        )

        can_edit = (
            lambda reservation: reservation.user == request.user
            or request.user.is_superuser
        )
        data = [
            {
                "title": "{room} ({user})".format(
                    room=room.name, user=r.user.get_full_name() or r.user.get_username()
                ),
                "room": room.name,
                "user": r.user.get_full_name() or r.user.get_username(),
                "start": str(r.from_date),
                "end": str(
                    r.to_date + timedelta(days=1)
                ),  # Because full-calendar events ;-)
                "url": can_edit(r) and reverse_lazy("reservations:edit", args=[r.id]),
                "owned": can_edit(r),
            }
            for r in reservations
        ]

        return JsonResponse(data, safe=False)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class TurnsPreparation(LoginRequiredMixin, FormView):
    http_method_names = ["get", "post"]
    form_class = TurnsPreparationForm
    template_name = "reservations/create_turns.html"

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""

        reservations = compute_turns(**form.cleaned_data)
        return render(
            self.request,
            "reservations/confirm_create_turns.html",
            context={
                "reservations": reservations,
                "form": TurnsCreationForm(form.cleaned_data),
            },
        )


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class TurnsCreation(SuccessMessageMixin, LoginRequiredMixin, FormView):
    http_method_names = ["get", "post"]
    form_class = TurnsCreationForm
    template_name = "reservations/confirm_create_turns.html"
    success_url = reverse_lazy("reservations:index")

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""

        reservations = compute_turns(**form.cleaned_data)
        all_rooms = Room.objects.all()
        for r in reservations.values():
            r.save()
            r.rooms.add(*all_rooms)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Turnos creados para el {}".format(cleaned_data["year"])
