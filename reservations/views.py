from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from reservations.models import Reservation
from reservations.forms import ReservationCreationForm


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
