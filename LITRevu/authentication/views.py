from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.conf import settings
from . import forms

# Fonction pour déconnecter l'utilisateur et rediriger vers la page de connexion.
def logout_user(request):
    logout(request)
    return redirect('login')

# Vue basé sur une classe pour gérer la page de connexion.
class LoginPageView(View):
    template_name = 'authentication/login.html'

# Méthode GET : affichage du formulaire de connexion.
    def get(self, request):
        """
        Détermine quel formulaire a été soumis en fonction du bouton cliqué.
        Vérifie si le formulaire est valide.
        Authentifie l'utilisateur avec le nom d'utilisateur et le mot de passe.
        Connecte l'utilisateur.
        Recrée les formulaire pour le rendu de la page après erreur.
        Rendu du template avec les formulaires et le message d'erreur
        """
        login_form_large = forms.LoginFormLarge()
        login_form_medium = forms.LoginFormMedium()
        return render(request, self.template_name, {
            'login_form_large': login_form_large, # Formulaire pour grand écran
            'login_form_medium': login_form_medium, # Formulaire pour petit écran
        })

# Méthode POST : traitement des données envoyés par le formulaire.
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

# Vue pour la page d'inscription.
def signup_page(request):
    """
    Récupère les données du formulaire.
    Crée l'utilisateur.
    Connecte automatiquement l'utilisateur après inscription.
    Redirige vers l'URL définie dans les paramètres.
    Rendu du template avec le formulaire et le message d'erreur si nécessaire.
    """
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
