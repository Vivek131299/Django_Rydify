from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import TravelDetails, Location, DriverAvailability


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    whatsapp_number = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'whatsapp_number', 'password1', 'password2']


class TravelDetailsForm(ModelForm):
    class Meta:
        model = TravelDetails
        exclude = ["customer"]

        widgets = {
            'date_of_arrival': forms.TextInput(attrs={'type': 'date'}),
            'time_of_arrival': forms.TextInput(attrs={'type': 'time'})
        }

    pickup = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    drop = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DriverRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class DriverAvailabilityForm(ModelForm):
    class Meta:
        model = DriverAvailability
        exclude = ["driver"]

        widgets = {
            'available_date': forms.TextInput(attrs={'type': 'date'}),
            'start_time': forms.TextInput(attrs={'type': 'time'}),
            'end_time': forms.TextInput(attrs={'type': 'time'})
        }

