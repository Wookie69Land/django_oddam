from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password

from .email import activate_user, check_token
from .tasks import send_activation_email_task, send_password_email_task

from oddam_app.models import Donation, Institution, Category
from oddam_app.forms import UserRegisterForm, UserPasswordForm, EditProfileForm, \
    UpdatePasswordForm, UserEmailForm, ResetPasswordForm


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


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories,
                                             'institutions': institutions})
    def post(self, request):
        categories_id = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=categories_id).distinct()
        quantity = request.POST.get('bags')
        institution = get_object_or_404(Institution, id=request.POST.get('organization'))
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        new_donation = Donation.objects.create(quantity=quantity,
                                               institution=institution,
                                               address=address,
                                               phone_number=phone_number,
                                               city=city,
                                               zip_code=zip_code,
                                               pick_up_date=pick_up_date,
                                               pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment,
                                               user=request.user)
        new_donation.categories.add(*categories)
        new_donation.save()
        return redirect('form-confirmation')


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class InstitutionAjaxView(View):
    def get(self, request):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            categories = request.GET.getlist('categories[]')
            institutions_query = Institution.objects.filter(categories__in=categories).distinct()
            institutions = []
            for i in institutions_query:
                institution = model_to_dict(i)
                del institution['categories']
                institutions.append(institution)
            data = render_to_string('institution_form.html', {'institutions': institutions})
            return JsonResponse(data, safe=False)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user.is_active)
        if not user.is_active:
            message = "Musisz aktywować konto. Sprawdź, czy nie dostałeś linka aktywacyjnego na email."
            return render(request, 'user_message.html', {'message': message})
        if user is not None:
            login(request, user)
            return redirect('start')
        return render(request, "login.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('start')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                password=password, email=email, is_active=False)
            send_activation_email_task(request, new_user)
            message = 'Dziękujemy za rejestrację. Na maila prześlemy link do aktywacji.'
            return render(request, 'user_message.html', {'message': message})

        else:
            return render(request, 'register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by('-pick_up_date')
        user_bags = 0
        institutions = []
        for donation in donations:
            user_bags += donation.quantity
            if donation.institution not in institutions:
                institutions.append(donation.institution)
        user_institutions = len(institutions)
        return render(request, 'profile.html', {'donations': donations,
                                                'user_bags': user_bags,
                                                'user_institutions': user_institutions})


class GoToEditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserPasswordForm()
        return render(request, 'password_form.html', {'form': form})
    def post(self, request):
        password = request.user.password
        form = UserPasswordForm(request.POST)
        if form.is_valid():
            password_to_check = form.cleaned_data.get('password')
            if check_password(password_to_check, password):
                return redirect('edit-profile')
        form = UserPasswordForm(request.POST)
        return render(request, 'password_form.html', {'form': form})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'edit_profile_form.html', {'form': form})
    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        form = EditProfileForm(request.POST, instance=request.user)
        return render(request, 'edit_profile_form.html', {'form': form})


class EditPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdatePasswordForm()
        return render(request, 'password_form.html', {'form': form})
    def post(self, request):
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            password = request.user.password
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('password')
            if check_password(old_password, password):
                user = request.user
                user.set_password(new_password)
                user.save()
                return redirect('login')
        return render(request, 'password_form.html', {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        success = activate_user(uidb64, token)
        if success:
            message = "Teraz możesz się zalogować."
            login_button = True
            return render(request, 'user_message.html', {'message': message,
                                                         'login_button': login_button})
        message = 'Nie udało się aktywować konta. Spróbuj jeszcze raz założyć konto.'
        return render(request, 'user_message.html', {'message': message})


class ForgottenPasswordView(View):
    def get(self, request):
        form = UserEmailForm()
        return render(request, 'email_form.html', {'form': form})
    def post(self, request):
        form = UserEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = get_object_or_404(User, email=email)
            send_password_email_task(request, user)
            message = 'Na maila prześlemy link do zmiany hasła.'
            return render(request, 'user_message.html', {'message': message})

        else:
            return render(request, 'register.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        success = check_token(uidb64, token)
        if success:
            form = ResetPasswordForm()
            return render(request, 'password_form.html', {'form': form})
        message = 'Nie udało się zresetować hasła. Spróbuj jeszcze raz.'
        return render(request, 'user_message.html', {'message': message})
    def post(self, request, uidb64, token):
        form = ResetPasswordForm(request.POST)
        user = check_token(uidb64, token)
        print(user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.save()
            message = "Teraz możesz się zalogować."
            login_button = True
            return render(request, 'user_message.html', {'message': message,
                                                         'login_button': login_button})
        message = 'Nie udało się zresetować hasła. Spróbuj jeszcze raz.'
        return render(request, 'user_message.html', {'message': message})


