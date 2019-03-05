from django.http import HttpResponse
from django.template import loader
from datetime import date

from reservations.models import Reservation


def index(request):
    template = loader.get_template("reservations/index.html")
    today = date.today()
    context = {
        "next": Reservation.objects.filter(from_date__gte=today),
        "past": Reservation.objects.filter(from_date__lt=today),
    }
    return HttpResponse(template.render(context, request))
