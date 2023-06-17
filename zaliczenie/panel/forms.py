from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Faktura, Ogloszenie

class CustomUserCreationForm(UserCreationForm):
    imie = forms.CharField(max_length=30)
    nazwisko = forms.CharField(max_length=30)
    adres = forms.CharField(max_length=100)
    nr_telefonu = forms.CharField(max_length=15)
    adres_email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'imie', 'nazwisko', 'adres', 'nr_telefonu', 'adres_email')


class CustomUserEditForm2(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'imie', 'nazwisko', 'adres', 'nr_telefonu', 'adres_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True



class FakturaForm(forms.ModelForm):
    class Meta:
        model = Faktura
        fields = ['username', 'typ', 'data', 'kwota', 'status']

class OgloszenieForm(forms.ModelForm):
    class Meta:
        model = Ogloszenie
        fields = ['tytul', 'tresc']