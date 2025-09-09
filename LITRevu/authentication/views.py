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
    login_form_class = forms.LoginForm

    def get(self, request):
        login_form = self.login_form_class()
        return render(request, self.template_name, {
            'login_form': login_form, 
        })

    def post(self, request):
        login_form = self.login_form_class(request.POST)
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
            message ="Formulaire de connexion invalide"
        return render(request, self.template_name, {
            'login_form': login_form,
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

