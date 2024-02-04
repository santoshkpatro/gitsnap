from django.contrib import admin
from django.urls import path

from gitsnap.views.home import IndexView, ProfileView
from gitsnap.views.accounts import LoginView
from gitsnap.views.projects.index import ProjectDetailView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="accounts-login"),
    path("<str:username>/", ProfileView.as_view(), name="home-profile"),
    path("<str:username>/<str:name>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("", IndexView.as_view(), name="home-index")
]
