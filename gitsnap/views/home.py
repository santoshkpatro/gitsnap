from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from gitsnap.models.user import User

class IndexView(View):
    def get(self, request):
        return render(request, "home/index.html")
    

class ProfileView(View):
    def get(self, request, username):
        user: User = User.objects.filter(username=username).first()
        if not user:
            raise Http404

        context = {
            "user": user
        }
        return render(request, "home/profile.html", context)