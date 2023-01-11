from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator

from oddam_app.models import Donation, Institution

class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        bags = 0
        institutions = []
        for donation in donations:
            bags += donation.quantity
            if donation.institution not in institutions:
                institutions.append(donation.institution)
        institutions_count = len(institutions)

        foundations = get_list_or_404(Institution, type=1)
        organizations = get_list_or_404(Institution, type=2)
        collections = get_list_or_404(Institution, type=3)
        paginator1 = Paginator(foundations, 3)
        paginator2 = Paginator(organizations, 3)
        paginator3 = Paginator(collections, 3)
        page1 = request.GET.get('page1')
        page2 = request.GET.get('page2')
        page3 = request.GET.get('page3')
        foundations = paginator1.get_page(page1)
        organizations = paginator2.get_page(page2)
        collections = paginator3.get_page(page3)

        return render(request, "index.html", {'bags': bags,
                                              'institutions': institutions_count,
                                              'foundations': foundations,
                                              'organizations': organizations,
                                              'collections': collections})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

