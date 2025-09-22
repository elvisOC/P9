from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.conf import settings
from . import forms


def logout_user(request):
    logout(request)
    return redirect('login')


class LoginPageView(View):
    template_name = 'authentication/login.html'

    def get(self, request):
        login_form_large = forms.LoginFormLarge()
        login_form_medium = forms.LoginFormMedium()
        return render(request, self.template_name, {
            'login_form_large': login_form_large,
            'login_form_medium': login_form_medium,
        })

    def post(self, request):
        if 'large-screen-submit' in request.POST:
            login_form = forms.LoginFormLarge(request.POST)
        elif 'medium-screen-submit' in request.POST:
            login_form = forms.LoginFormMedium(request.POST)
        else:
            login_form = forms.LoginFormLarge(request.POST)

        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'].lower(),
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = "Identifiants invalides."
        else:
            message = "Formulaire de connexion invalide"

        login_form_large = forms.LoginFormLarge()
        login_form_medium = forms.LoginFormMedium()

        return render(request, self.template_name, {
            'login_form_large': login_form_large,
            'login_form_medium': login_form_medium,
            'message': message
        })


def signup_page(request):
    signup_form = forms.SignUpForm(request.POST)
    if signup_form.is_valid():
        user = signup_form.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        message = "Formulaire d'inscription invalide"
    return render(request, 'authentication/signup.html', {
        'signup_form': signup_form,
        'message': message
    })
