from django.urls import path

from profiles.views import EditProfile

app_name = "profiles"
urlpatterns = [path("<int:pk>/", EditProfile.as_view(), name="edit")]
