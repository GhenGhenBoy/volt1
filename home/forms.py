from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Contact, Profile


class ContactForm(forms.ModelForm):
   class Meta:
      model = Contact
      fields = ['full_name','phone','email','message']


class SignupForm(UserCreationForm):
   username: forms.CharField(max_length= 50)
   first_name = forms.CharField(max_length=100)
   last_name = forms.CharField(max_length=100)
   email = forms.EmailField(max_length=150)

   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileUpdate(forms.ModelForm):
   class Meta:
      model = Profile
      fields = ['first_name','last_name','email','phone','address','state', 'img']
      widgets = {
         'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
         'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
         'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
         'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
         'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'address'}),
         'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
         'img':forms.FileInput(attrs={'class':'form-control'}),
      }