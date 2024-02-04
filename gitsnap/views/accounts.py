from django.views import View
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages

from gitsnap.models.user import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            messages.warning(request, "Invalid input provided")
            return redirect("accounts-login")
        
        data = form.cleaned_data
        if '@' in data.get("username"):
            kwargs = {"email": data.get("username")}
        else:
            kwargs = {"username": data.get("username")}

        user: User = User.objects.filter(**kwargs).first()
        if not user:
            messages.warning(request, "No user exists with the given username or email address.")
            return redirect("accounts-login")

        if not user.check_password(data.get("password")):
            messages.warning(request, "Please enter valid password.")
            return redirect('accounts-login')
        
        login(request, user)
        return redirect(to='home-profile', username=user.username)
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        pass