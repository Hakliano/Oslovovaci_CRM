from django.contrib import admin
from .models import Partner, ZpusobOsloveni, Level, Reakce, PartnerDetail, Osloveni

# Registrace modelů do administrace
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'jednatel', 'email', 'telefon', 'adresa', 'instagram', 'facebook')
    search_fields = ('jmeno', 'email', 'telefon')

@admin.register(ZpusobOsloveni)
class ZpusobOsloveniAdmin(admin.ModelAdmin):
    list_display = ('nazev',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('nazev',)

@admin.register(Reakce)
class ReakceAdmin(admin.ModelAdmin):
    list_display = ('nazev',)

@admin.register(PartnerDetail)
class PartnerDetailAdmin(admin.ModelAdmin):
    list_display = ('partner', 'zpusob_osloveni', 'level', 'reakce')
    list_filter = ('zpusob_osloveni', 'level', 'reakce')


@admin.register(Osloveni)
class OsloveniAdmin(admin.ModelAdmin):
    list_display = ('datum', 'partner', 'zpusob_osloveni', 'reakce', 'user')
    list_filter = ('datum', 'zpusob_osloveni', 'reakce', 'user')
    search_fields = ('partner__jmeno', 'zpusob_osloveni__nazev', 'reakce__nazev')
