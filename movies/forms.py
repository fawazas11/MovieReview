
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie,Genre


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = [
            'title',
            'description',
            'release_year',
            'director',
            'genre',
            'poster',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie description',
                'rows': 4
            }),

            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter release year'
            }),

            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter director name'
            }),

            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),

            'poster': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter genre name'
            })
        }