# Generated by Django 2.1.7 on 2019-03-04 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("rooms", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={
                "ordering": ["name"],
                "verbose_name": "Habitación",
                "verbose_name_plural": "Habitaciones",
            },
        )
    ]