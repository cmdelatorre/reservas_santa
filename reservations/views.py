from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import BaseDetailView

from reservations.models import Reservation
from reservations.forms import ReservationCreationForm
from rooms.models import Room


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


class ReservationCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = Reservation
    form_class = ReservationCreationForm
    # fields = ["from_date", "to_date", "rooms", "notes"]
    template_name = "reservations/create.html"
    success_url = reverse_lazy("reservations:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationEdit(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = Reservation
    form_class = ReservationCreationForm
    # fields = ["from_date", "to_date", "rooms", "notes"]
    template_name = "reservations/create.html"
    success_url = reverse_lazy("reservations:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy("login")
    model = Reservation
    success_url = reverse_lazy("reservations:index")


class RoomReservations(BaseDetailView):
    model = Room
    http_method_names = ["get"]
    pk_url_kwarg = "room_id"

    def get(self, request, room_id):
        room = self.get_object()
        params = self.request.GET
        reservations = room.filter_reservations_that_intersect(
            params["start"], params["end"]
        )

        data = [
            {
                "title": "{room} ({user})".format(
                    room=room.name, user=r.user.get_full_name() or r.user.get_username()
                ),
                "start": str(r.from_date),
                "end": str(
                    r.to_date + timedelta(days=1)
                ),  # Because full-calendar events ;-)
            }
            for r in reservations
        ]

        return JsonResponse(data, safe=False)
