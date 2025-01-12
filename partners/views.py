from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Osloveni, Partner, ZpusobOsloveni, Level, Reakce, PartnerDetail, ZpusobOsloveni
from django.utils import timezone
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages



def logoutpage(request):
    return render(request, 'logout.html')

# Funkce pro přidání nového partnera
@login_required
def add_partner(request):
    # Načtení všech partnerů (základní queryset)
    partners = Partner.objects.all()

    # Získání hodnoty filtru z GET parametrů
    partner_name = request.GET.get('partner', None)

    # Filtrování podle jména partnera
    if partner_name:
        partners = partners.filter(jmeno__icontains=partner_name)

    if request.method == 'POST' and 'add_partner_form' in request.POST:
        # Zpracování formuláře pro přidání nového partnera
        jmeno = request.POST.get('jmeno')
        jednatel = request.POST.get('jednatel')
        email = request.POST.get('email')
        telefon = request.POST.get('telefon')
        adresa = request.POST.get('adresa')
        instagram = request.POST.get('instagram')
        facebook = request.POST.get('facebook')

        # Uložení nového partnera do databáze
        partner = Partner.objects.create(
            jmeno=jmeno,
            jednatel=jednatel,
            email=email,
            telefon=telefon,
            adresa=adresa,
            instagram=instagram,
            facebook=facebook,
            created_by=request.user
        )

        # Nastavení výchozí hodnoty pro způsob oslovení
        default_zpusob = ZpusobOsloveni.objects.get(nazev="Zatím nic")
        PartnerDetail.objects.create(
            partner=partner,
            zpusob_osloveni=default_zpusob,
            level=None,
            reakce=None
        )

        # Přidání zprávy o úspěšném přidání
        messages.success(request, f"Partner {jmeno} byl úspěšně přidán.")

        # Přesměrování s uchováním hodnoty filtru (pokud existuje)
        redirect_url = f"{request.path}?partner={partner_name}" if partner_name else request.path
        return redirect(redirect_url)

    # Kontext pro šablonu
    context = {
        'partners': partners,
        'partner_name': partner_name,  # Vracíme aktuální hodnotu filtru pro šablonu
    }

    # Vykreslení šablony
    return render(request, 'add_partner.html', context)

# Funkce pro výpis partnerů a editaci detailů
@login_required

def partner_list(request):
    # Získání hodnot filtrů z GET parametrů
    zpusob_id = request.GET.get('zpusob_osloveni', None)
    level_id = request.GET.get('level', None)
    reakce_id = request.GET.get('reakce', None)
    osloven = request.GET.get('osloven', None)  # Nový filtr pro oslovení
    partner_name = request.GET.get('partner', None)  # Filtr podle jména
    adresa = request.GET.get('adresa', None)  # Filtr podle města
    per_page = request.GET.get('per_page', 10)

    # Zajistěte, že per_page je číslo
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    # Základní queryset
    partners = Partner.objects.all()

    # Aplikace filtrů
    if zpusob_id:
        partners = partners.filter(partnerdetail__zpusob_osloveni_id=zpusob_id)
    if level_id:
        partners = partners.filter(partnerdetail__level_id=level_id)
    if reakce_id:
        partners = partners.filter(partnerdetail__reakce_id=reakce_id)
    if osloven:  # Ověření existence filtru
        if osloven == "yes":
            partners = partners.filter(osloveni__isnull=False)
        elif osloven == "no":
            partners = partners.filter(osloveni__isnull=True)
    if partner_name:  # Filtr podle jména
        partners = partners.filter(jmeno__icontains=partner_name)
    if adresa:
        adresa = adresa.strip().lower()
        partners = partners.filter(adresa__icontains=adresa)

    # Paginátor na filtrovaný queryset
    paginator = Paginator(partners, per_page)
    page_number = request.GET.get('page')  # Číslo stránky z URL
    page_obj = paginator.get_page(page_number)

    # Načtení pomocných dat pro šablonu
    zpusoby_osloveni = ZpusobOsloveni.objects.all()
    levels = Level.objects.all()
    reakce = Reakce.objects.all()

    # Zajištění výchozích detailů partnerů
    for partner in partners:
        PartnerDetail.objects.get_or_create(
            partner=partner,
            defaults={
                'zpusob_osloveni': ZpusobOsloveni.objects.get_or_create(nazev="Zatím nic")[0],
                'level': None,
                'reakce': None
            }
        )

    # Přidání posledního oslovení pro každého partnera
    for partner in partners:
        posledni_osloveni = partner.osloveni.order_by('-datum').first()
        partner.posledni_osloveni = posledni_osloveni

    # Kontext pro šablonu
    context = {
        'page_obj': page_obj,
        'partners': partners,
        'zpusoby_osloveni': zpusoby_osloveni,
        'levels': levels,
        'reakce': reakce,
        'osloven_filter': osloven,
        'partner_name': partner_name,
        'adresa': adresa,
        'per_page': per_page,
        'timestamp': datetime.now().timestamp(),  # Přidání dynamického timestampu

    }

    # Zpracování POST požadavku (uložení dat)
    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        zpusob_id = request.POST.get('zpusob_osloveni')
        level_id = request.POST.get('level')
        reakce_id = request.POST.get('reakce')

        if partner_id and zpusob_id and level_id and reakce_id:
            partner = Partner.objects.get(id=partner_id)
            zpusob_osloveni = ZpusobOsloveni.objects.get(id=zpusob_id)
            level = Level.objects.get(id=level_id)
            reakce = Reakce.objects.get(id=reakce_id)

            # Uložení nebo aktualizace PartnerDetail
            PartnerDetail.objects.update_or_create(
                partner=partner,
                defaults={
                    'zpusob_osloveni': zpusob_osloveni,
                    'level': level,
                    'reakce': reakce,
                }
            )
            print(f"Uloženo: {partner.jmeno}, Způsob: {zpusob_osloveni.nazev}, Level: {level.nazev}, Reakce: {reakce.nazev}")
        else:
            print("Některá data nejsou vyplněna!")

        # Přesměrování zpět na partner_list po uložení
        return redirect('partner_list')

    # Vykreslení šablony
    return render(request, 'partner_list.html', context)


# Funkce pro filtrování partnerů
@login_required

def filter_partners(request):
    partners = Partner.objects.select_related('partnerdetail__zpusob_osloveni', 'partnerdetail__level', 'partnerdetail__reakce').all()
    zpusoby_osloveni = ZpusobOsloveni.objects.all()
    levels = Level.objects.all()
    reakce = Reakce.objects.all()

    # Získání filtrů z GET parametrů
    zpusob_id = request.GET.get('zpusob_osloveni')
    level_id = request.GET.get('level')
    reakce_id = request.GET.get('reakce')
    osloven = request.GET.get('osloven')  # Nový filtr pro oslovení
    partner_name = request.GET.get('partner')  # Nový filtr pro jméno partnera


    # Základní queryset
    partners = Partner.objects.all()

    # Aplikace filtrů
    if zpusob_id:
        partners = partners.filter(partnerdetail__zpusob_osloveni_id=zpusob_id)
    if level_id:
        partners = partners.filter(partnerdetail__level_id=level_id)
    if reakce_id:
        partners = partners.filter(partnerdetail__reakce_id=reakce_id)
    if osloven:  # Ověření existence filtru
        if osloven == "yes":
            partners = partners.filter(osloveni__isnull=False)
        elif osloven == "no":
            partners = partners.filter(osloveni__isnull=True)
    if partner_name:  # Filtr podle jména
        partners = partners.filter(jmeno__icontains=partner_name)
    
    context = {
        'partners': partners,
        'zpusoby_osloveni': zpusoby_osloveni,
        'levels': levels,
        'reakce': reakce,
        'osloven_filter': osloven,
        'partner_name': partner_name,  


    }
    return render(request, 'partner_filter.html', context)



@login_required

def add_osloveni(request):
    partners = Partner.objects.all()
    zpusoby_osloveni = ZpusobOsloveni.objects.all()
    reakce_list = Reakce.objects.all()

    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        description = request.POST.get('description')
        content_sms = request.POST.get('content_sms')
        subject_email = request.POST.get('subject_email')
        content_email = request.POST.get('content_email')
        content_call = request.POST.get('content_call')
        reakce_id = request.POST.get('reakce')

        if partner_id and reakce_id:
            # Vytvoření záznamu oslovení
            partner = Partner.objects.get(id=partner_id)
            reakce = Reakce.objects.get(id=reakce_id)
            Osloveni.objects.create(
                datum=timezone.now(),
                partner=partner,
                reakce=reakce,
                user=request.user,
                description=description
            )
            return redirect('add_osloveni')

    context = {
        'partners': partners,
        'zpusoby_osloveni': zpusoby_osloveni,
        'reakce_list': reakce_list,
    }
    return render(request, 'add_osloveni.html', context)


def index(request):
    # Uživatelské stats    
    user_stats = user_statistics(request)

    # Celkový počet partnerů
    total_partners = Partner.objects.count()
    
    # Počet partnerů oslovených SMS, Emailem a Telefonicky
    sms_responded = PartnerDetail.objects.filter(zpusob_osloveni__nazev="SMS").count()
    email_responded = PartnerDetail.objects.filter(zpusob_osloveni__nazev="Email").count()
    call_responded = PartnerDetail.objects.filter(zpusob_osloveni__nazev="Hlas").count()
    not_contacted = PartnerDetail.objects.filter(zpusob_osloveni__nazev="Zatím nic").count()

    # Počet zbývajících partnerů k oslovení
    not_contacted = total_partners - (sms_responded + email_responded + call_responded)

    # Počet partnerů podle levelu
    level_zero = PartnerDetail.objects.filter(level__nazev="0").count()
    level_paid = PartnerDetail.objects.filter(level__nazev__gt="0").count()

    # Aktuální datum a čas
    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    # Poslání dat do šablony
    context = {
        'total_partners': total_partners,
        'sms_responded': sms_responded,
        'email_responded': email_responded,
        'call_responded': call_responded,
        'not_contacted': not_contacted,
        'level_zero': level_zero,
        'level_paid': level_paid,
        'current_datetime': current_datetime,
        'user_stats': user_stats,

    }

    return render(request, 'index.html', context)


@login_required

def partners_summary(request):
    partners = Partner.objects.all()

    # Načtení posledního oslovení pro každého partnera
    for partner in partners:
        posledni_osloveni = Osloveni.objects.filter(partner=partner).order_by('-datum').first()
        partner.posledni_osloveni = posledni_osloveni

    context = {
        'partners': partners
    }
    return render(request, 'partners_summary.html', context)


@login_required

def osloveni_detail (request, osloveni_id):
    osloveni = get_object_or_404(Osloveni, id=osloveni_id)
    context = {
        'osloveni': osloveni
    }
    return render(request, 'osloveni_detail.html', context)


@login_required

def user_statistics(request):
    users = User.objects.annotate(
        total_contacts=Count('osloveni'),  # Počet všech kontaktů
        successful_contacts=Count('osloveni', filter=Q(osloveni__reakce__nazev="Placená")),  # Úspěšné kontakty
        created_partners=Count('partner', distinct=True)  # Kolik partnerů uživatel přidal
    )

    # Pokud chceš pracovat jen s aktuálním uživatelem:
    current_user_stats = users.filter(id=request.user.id)

    return users

def delete_partner(request):
    if request.method == "POST":
        partner_id = request.POST.get('partner_id')
        if partner_id:
            partner = get_object_or_404(Partner, id=partner_id)
            partner_name = partner.jmeno
            partner.delete()
            return render(request, 'partner_delete_success.html', {'partner_name': partner_name})
    return redirect('partner_list')  # Pokud není POST, přesměruj zpět na seznam