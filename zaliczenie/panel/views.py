from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, FakturaForm, OgloszenieForm, CustomUserEditForm2
from .models import Faktura, CustomUser, Ogloszenie

from django.views.decorators.csrf import ensure_csrf_cookie

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return render(request, 'login.html', {'error_message': 'Niepoprawne dane logowania'})
    else:
        return render(request, 'login.html', {'request': request})

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def panel(request):
    if request.user.is_superuser:
        return redirect('management_panel')
    user = request.user
    ogloszenia = Ogloszenie.objects.all()
    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'ogloszenia': ogloszenia
    }
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('login')
    return render(request, 'user/panel.html', context)
def management_panel(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/management_panel.html', {'users': users})
def faktury(request):
    if request.user.is_superuser:
        moje_faktury = Faktura.objects.all()
        return render(request, 'admin/faktury.html', {'moje_faktury': moje_faktury})

    custom_user = request.user
    moje_faktury = Faktura.objects.filter(username=custom_user)
    if moje_faktury.exists():
        return render(request, 'user/faktury.html', {'moje_faktury': moje_faktury})
    else:
        komunikat = "Brak dostępnych faktur"
        return render(request, 'user/faktury.html', {'komunikat': komunikat})
def dodaj_fakture(request):
    if request.method == 'POST':
        form = FakturaForm(request.POST)
        if form.is_valid():
            Faktura = form.save()
            return redirect('sukces')
    else:
        form = FakturaForm()
    context = {'form': form}
    return render(request, 'admin/dodaj_fakture.html', context)
def sukces(request):
    return render(request, 'admin/sukces.html')
def edytuj_fakture(request, id):
    faktura = Faktura.objects.get(nr_faktury=id)
    if request.method == 'POST':
        form = FakturaForm(request.POST, instance=faktura)
        if form.is_valid():
            form.save()
            return redirect('admin/faktury')
    else:
        form = FakturaForm(instance=faktura)
    return render(request,
                'admin/edytuj_element.html',
                {'form': form})
def usun_fakture(request, id):
    faktura = Faktura.objects.get(nr_faktury=id)
    if request.method == 'POST':
        faktura.delete()
        return redirect('faktury')
    return render(request,
                    'admin/usun_element.html',
                    {'element': faktura})
def ogloszenia(request):
    ogloszenia = Ogloszenie.objects.all()
    context = {
        'ogloszenia': ogloszenia
    }
    if request.user.is_superuser:
        return render(request, 'admin/ogłoszenia.html', context)
    else:
        return render(request, 'user/ogloszenia.html', context)
def dodaj_ogloszenie(request):
    if request.method == 'POST':
        form = OgloszenieForm(request.POST)
        if form.is_valid():
            ogloszenie = form.save()
            return redirect('sukces_ogloszenia')
    else:
        form = OgloszenieForm()
        context = {'form': form}
    return render(request, 'admin/dodaj_ogloszenie.html', context)

def sukces_ogloszenia(request):
    return render(request, 'admin/sukces_ogloszenia.html')
def edytuj_ogloszenie(request, id):
    ogloszenie = Ogloszenie.objects.get(id=id)
    if request.method == 'POST':
        form = OgloszenieForm(request.POST, instance=ogloszenie)
        if form.is_valid():
            form.save()
            return redirect('ogloszenia')
    else:
        form = OgloszenieForm(instance=ogloszenie)
    return render(request,
                'admin/edytuj_element.html',
                {'form': form})
def usun_ogloszenie(request, id):
    ogloszenie = Ogloszenie.objects.get(id=id)
    if request.method == 'POST':
        ogloszenie.delete()
        return redirect('ogloszenia')
    return render(request,
                    'admin/usun_element.html',
                    {'element': ogloszenie})
def szczegoly_uzytkownika(request, id):
    user = get_object_or_404(CustomUser, id=id)
    context = {'user': user}
    if request.user.is_superuser:
        return render(request, 'admin/szczegoly_uzytkownika.html', context)
    else:
        return render(request, 'user/szczegoly_uzytkownika.html', context)
def edytuj_uzytkownika(request, id):
    uzytkownik = CustomUser.objects.get(id=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CustomUserEditForm2(request.POST, instance=uzytkownik)
            if form.is_valid():
                form.save()
                return redirect('management_panel')
        else:
            form = CustomUserEditForm2(instance=uzytkownik)
        return render(request,
                    'admin/edytuj_element.html',
                    {'form': form})
    else:
        if request.method == 'POST':
            form = CustomUserEditForm2(request.POST, instance=uzytkownik)
            if form.is_valid():
                form.save()
                return redirect('szczegoly_uzytkownika',uzytkownik.id)
        else:
            form = CustomUserEditForm2(instance=uzytkownik)
        return render(request,
                    'user/edytuj_element.html',
                    {'form': form})

def usun_uzytkownika(request, id):
    uzytkownik = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        uzytkownik.delete()
        return redirect('management_panel')
    return render(request,
                    'admin/usun_element.html',
                    {'element': uzytkownik})