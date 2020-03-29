from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wants_emails = models.BooleanField(verbose_name="recibir emails?", default=False)
