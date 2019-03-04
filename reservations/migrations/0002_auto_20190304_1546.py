# Generated by Django 2.1.7 on 2019-03-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_auto_20190304_1540"),
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="reservation", name="room"),
        migrations.AddField(
            model_name="reservation",
            name="rooms",
            field=models.ManyToManyField(
                related_name="reservas",
                to="rooms.Room",
                verbose_name="Habitación reservada",
            ),
        ),
    ]
