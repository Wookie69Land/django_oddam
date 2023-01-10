from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator


class LandingPageView(View):
    def get(self, request):
        return render(request, "index.html")


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

