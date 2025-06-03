from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
