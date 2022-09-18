from rooms.models import Room

Room.objects.bulk_create(
    [
        Room(name="pieza de Manina"),
        Room(name="pieza de la pileta"),
        Room(name="pieza del monturero"),
        Room(name="pieza del alto"),
        Room(name="pieza de las cocina"),
    ],
    ignore_conflicts=True,
)
