from django import forms 
from . import models



class ticketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'neumorphic neumorphic-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'neumorphic neumorphic-input',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label='Rating'
    )

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'neumorphic neumorphic-input',
            }),
            'body': forms.Textarea(attrs={
                'class': 'neumorphic neumorphic-input',
            }),
        }
        
class search_user(forms.Form):
    query = forms.CharField(
    max_length=63,
    label="Suivre d'autres utilisateurs",
    widget=forms.TextInput(attrs={
        'placeholder': "Nom d'utilisateur",
        'class': 'neumorphic neumorphic-input'
        })
    )