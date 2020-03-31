from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import Http404

from profiles.forms import UserProfileForm
from profiles.models import Profile


class EditProfile(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = Profile
    template_name = "profiles/profile_edit.html"
    success_url = reverse_lazy("home")
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("No tenés permiso para editar estas preferencias")
        return obj

    #
    # def get_context_data(self, **kwargs):
    #     """Insert the form into the context dict."""
    #     import ipdb; ipdb.set_trace()
    #     return super().get_context_data(**kwargs)
