from django.contrib import admin
from cuser.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from profiles.models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
