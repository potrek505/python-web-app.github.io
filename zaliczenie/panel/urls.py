from django.urls import path
from . import views
from .views import management_panel

urlpatterns = [

    path('', views.panel, name='panel'),
    path('faktury/', views.faktury, name='faktury'),
    path('logout/', views.logout_view, name='logout'),
    path('management_panel/', management_panel, name='management_panel'),
    path('faktury/dodaj-fakture/', views.dodaj_fakture, name='dodaj_fakture'),
    path('sukces/', views.sukces, name='sukces'),
    path('faktury/<int:id>/edytuj/', views.edytuj_fakture, name='edytuj_fakture'),
    path('ogloszenia/<int:id>/edytuj/', views.edytuj_ogloszenie, name='edytuj_ogloszenie'),
    path('faktura/<int:id>/usun/', views.usun_fakture, name='usun_fakture'),
    path('ogloszenia/dodaj-ogloszenie/', views.dodaj_ogloszenie, name='dodaj_ogloszenie'),
    path('ogloszenia/', views.ogloszenia, name='ogloszenia'),
    path('ogloszenia/<int:id>/usun/', views.usun_ogloszenie, name='usun_ogloszenie'),
    path('szczegoly/<int:id>/', views.szczegoly_uzytkownika, name='szczegoly_uzytkownika'),
    path('management_panel/<int:id>/edytuj/', views.edytuj_uzytkownika, name='edytuj_uzytkownika'),
    path('management_panel/<int:id>/usun/', views.usun_uzytkownika, name='usun_uzytkownika'),
    path('faktury/dodaj-fakture/sukces/', views.sukces, name='sukces'),
    path('ogloszenia/dodaj-ogloszenie/sukces/', views.sukces_ogloszenia, name='sukces_ogloszenia'),

]