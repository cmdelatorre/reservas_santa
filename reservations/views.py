from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
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
        context["next"] = Reservation.objects.filter(from_date__gte=today)
        context["past"] = Reservation.objects.filter(from_date__lt=today)
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


class RoomReservations(BaseDetailView):
    model = Room
    http_method_names = ["get"]
    pk_url_kwarg = "room_id"

    def get(self, request, room_id):
        room = self.get_object()
        params = self.request.GET
        reservations = room.filter_reservations(params["start"], params["end"])

        data = [
            {
                "title": "{room} ({user})".format(
                    room=room.name, user=r.user.get_full_name()
                ),
                "start": str(r.from_date),
                "end": str(r.to_date),
            }
            for r in reservations
        ]

        return JsonResponse(data, safe=False)
