from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    adres = models.CharField(max_length=255)
    nr_telefonu = models.CharField(max_length=20)
    adres_email = models.EmailField()
class Faktura(models.Model):
  username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)
  nr_faktury = models.AutoField(primary_key=True)
  typ = models.CharField(max_length=255)
  data = models.DateField()
  kwota = models.IntegerField()
  status = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.nr_faktury} - {self.username} - {self.typ} - {self.data} - {self.kwota}zł - {self.status}"

class Ogloszenie(models.Model):
    tytul = models.CharField(max_length=255)
    tresc = models.TextField()
    data = models.DateField(auto_now_add=True)