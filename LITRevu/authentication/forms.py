from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Formulaire de connexion de base.
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
            'class': 'neumorphic neumorphic-input'
        })
    )
    password = forms.CharField(
        max_length=63,
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe",
            'class': 'neumorphic neumorphic-input'
        })
    )


# Formulaire de connexion pour grand écran (hérite de LoginForm).
class LoginFormLarge(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'id_username_large'})
        self.fields['password'].widget.attrs.update({'id': 'id_password_large'})


# Formulaire de connexion pour écran moyen (hérite de LoginForm).
class LoginFormMedium(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'id_username_medium'})
        self.fields['password'].widget.attrs.update({'id': 'id_password_medium'})


# Formulaire d'inscription
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=63,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
            'class': 'neumorphic neumorphic-input'
        })
    )
    password1 = forms.CharField(
        max_length=63,
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe",
            'class': 'neumorphic neumorphic-input'
        })
    )
    password2 = forms.CharField(
        max_length=63,
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Confirmer le mot de passe",
            'class': 'neumorphic neumorphic-input'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
