from django.db import migrations
from django.conf import settings


def create_user_profiles(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = settings.AUTH_USER_MODEL
    User = apps.get_model("cuser", "CUser")
    Profile = apps.get_model("profiles", "Profile")

    Profile.objects.bulk_create(
        Profile(user=u) for u in User.objects.filter(profile__isnull=True)
    )


def delete_user_profiles(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    Profile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("profiles", "0001_initial"), ("cuser", "0001_initial")]

    operations = [migrations.RunPython(create_user_profiles, delete_user_profiles)]
