from django.views import View
from django.shortcuts import render
from django.contrib import messages

from gitsnap.mixins import ProjectPermissionMixin


class ProjectDetailView(ProjectPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        messages.warning(request, "This project has been archived. No updates are being worked on this")
        return render(request, "projects/detail.html")