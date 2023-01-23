"""project_oddam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from oddam_app.views import LandingPageView, AddDonationView, LoginView, \
    RegisterView, LogoutView, InstitutionAjaxView, FormConfirmationView, \
    ProfileView, GoToEditProfileView, EditProfileView, EditPasswordView, \
    ActivateAccountView, ForgottenPasswordView, ResetPasswordView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='start'),
    path('add_donation/', AddDonationView.as_view(), name='donation'),
    path('ajax/institutions/', InstitutionAjaxView.as_view(), name='ajax-institutions'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('donation_confirmation/', FormConfirmationView.as_view(), name='form-confirmation'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/go-to-edit/', GoToEditProfileView.as_view(), name='go-to-profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/password/', EditPasswordView.as_view(), name='edit-password'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    path('forgotten/password/', ForgottenPasswordView.as_view(), name='forgotten-password'),
    path('reset_password/<uidb64>/<token>', ResetPasswordView.as_view(), name='reset-password'),
]
