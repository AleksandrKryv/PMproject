from django import forms
from django.db import models
from django.forms import ModelForm, Form
from .models import PMuser, Photograph, Model, Album, Portfolio, Comment, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

class PMuserForm(ModelForm):
    class Meta:
        model = PMuser
        fields = ('username', 'password', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                               "Enter username"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':
                                                   "Enter password with at least 8 digits"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':
                                             "Enter your email"
                                             }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                   "Enter your phone number"
                                                   }),


        }



    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if PMuser.objects.filter(phone_number=data):
            raise forms.ValidationError("Phone number already exists")
        return data


class ExtendRegistrationForm(ModelForm):
    class Meta:
        model = PMuser
        fields = ('first_name', 'last_name', 'gender', 'age', 'country', 'city', 'preferences')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                "Enter your first name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                "Enter your last name"}),
            'gender': forms.Select(attrs={'class': 'form-control'
                                          }),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                "Enter your age"}),
            'country': forms.Select(attrs={'class': 'form-control',
                                           }),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                "Enter your city"}),
            'preferences': forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                "Enter your preferences "}),

        }


class PhotographForm(ModelForm):
    class Meta:
        model = Photograph
        fields = ('about', 'experience', 'level', 'conditions',)
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                           "Add here some information about yourself"}),
            'experience': forms.Select(attrs={'class': 'form-control',
                                              }),
            'level': forms.Select(attrs={'class': 'form-control',
                                         }),
            'conditions': forms.Select(attrs={'class': 'form-control',
                                              }),
        }


class Modelform(ModelForm):
    class Meta:
        model = Model
        fields = ('about', 'experience', 'level', 'conditions',
                  'height', 'hair_length', 'hair_color', 'eye_color',
                  'body_type', 'skin_tone',)
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                           "Add here some information about yourself"}),
            'experience': forms.Select(attrs={'class': 'form-control',
                                              }),
            'level': forms.Select(attrs={'class': 'form-control',
                                         }),
            'conditions': forms.Select(attrs={'class': 'form-control',
                                              }),
            'height': forms.Select(attrs={'class': 'form-control',
                                              }),
            'hair_length': forms.Select(attrs={'class': 'form-control',
                                              }),
            'hair_color': forms.Select(attrs={'class': 'form-control',
                                              }),
            'eye_color': forms.Select(attrs={'class': 'form-control',
                                              }),
            'body_type': forms.Select(attrs={'class': 'form-control',
                                              }),
            'skin_tone': forms.Select(attrs={'class': 'form-control',
                                              }),

        }


class LoginForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':
        "Enter password with at least 8 digits"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                               "Enter your username"}))

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        return username


class AlbumaddForm(forms.Form):

    album_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                            "Enter album name"}) )
    description = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                            }))

class PortfolioaddForm(forms.Form):
    description = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))






