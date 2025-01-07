from django.db import models
from django.contrib.auth.models import User  # Import pro Django uživatele

# Model pro údaje o partnerovi
class Partner(models.Model):
    jmeno = models.CharField(max_length=100)
    jednatel = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=15)
    adresa = models.CharField(max_length=200)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Kdo partnera přidal

    def __str__(self):
        return self.jmeno

# Model pro způsob oslovení
class ZpusobOsloveni(models.Model):
    nazev = models.CharField(max_length=50)  # SMS, hlas, email, atd.

    def __str__(self):
        return self.nazev

# Model pro level
class Level(models.Model):
    nazev = models.CharField(max_length=10)  # Nic, 0,1,2,3,4,5

    def __str__(self):
        return self.nazev

# Model pro reakci
class Reakce(models.Model):
    nazev = models.CharField(max_length=50)  # Zdarma, placená, žádná, atd.

    def __str__(self):
        return self.nazev

# Spojovací tabulka
class PartnerDetail(models.Model):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='partnerdetail')
    zpusob_osloveni = models.ForeignKey(ZpusobOsloveni, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    reakce = models.ForeignKey(Reakce, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.partner.jmeno} - {self.zpusob_osloveni.nazev} - {self.level.nazev} - {self.reakce.nazev}"



class Osloveni(models.Model):
    datum = models.DateTimeField(auto_now_add=True)  # Datum a čas oslovení
    zpusob_osloveni = models.ForeignKey('ZpusobOsloveni', on_delete=models.SET_NULL, null=True)
    reakce = models.ForeignKey('Reakce', on_delete=models.SET_NULL, null=True)
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, related_name='osloveni')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)  # Nové pole pro poznámky

    def __str__(self):
        return f"Oslovení: {self.partner.jmeno} - {self.zpusob_osloveni.nazev} ({self.datum})"
