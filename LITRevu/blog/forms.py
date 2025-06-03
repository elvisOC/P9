from django import forms 
from . import models



class ticketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'neumorphic neumorphic-input',
                'placeholder': 'Titre du ticket'
            }),
            'description': forms.Textarea(attrs={
                'class': 'neumorphic neumorphic-input',
                'placeholder': 'Description'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }