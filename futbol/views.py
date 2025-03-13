from django.shortcuts import render, redirect
from django import forms
from futbol.models import *
from django.db.models import Count, Q


# Create your views here.

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"

def nou_jugador(request):
    form = JugadorForm()
    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taula_pichichis')
    return render(request, "menu.html",{
                    "form": form,
            })

def taula_pichichis(request):
    jugadors = Jugador.objects.annotate(gols=Count('event__tipus_esdeveniment', filter=Q(event__tipus_esdeveniment='gol'))).order_by('-gols')
    return render(request, "taula_pichichis.html", {
        "jugadors": jugadors,
    })

def taula_partits(request):
    equips = Equip.objects.all()
    partits = Partit.objects.all()

    # Crear una matriz vacía para almacenar los resultados
    resultats = []
    # Agregar la fila de encabezados
    fila_encabezados = [""] + [equip.nom for equip in equips]
    resultats.append(fila_encabezados)

    for equip_local in equips:
        fila = [equip_local.nom]
        for equip_visitant in equips:
            # Buscar el partido correspondiente
            partido = partits.filter(equip_local=equip_local, equip_visitant=equip_visitant).first()
            if partido:
                # Agregar el resultado del partido a la fila
                fila.append(f"{partido.gols_local()} - {partido.gols_visitant()}")
            else:
                # Si no hay partido, agregar un valor vacío
                fila.append("")
        resultats.append(fila)

    return render(request, "taula_partits.html", {
        "resultats": resultats,
    })

def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def classificacio(request,lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        # contar goles
        gols_favor = 0
        gols_contra = 0
        # contar victorias, derrotas y empates
        victories = 0
        derrotes = 0
        empats = 0

        for partit in lliga.partits.filter(equip_local=equip):
            gols_favor += partit.gols_local()
            gols_contra += partit.gols_visitant()
            if partit.gols_local() > partit.gols_visitant():
                # victoria
                victories += 1
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                # empate
                empats += 1
                punts += 1
            else:
                # derrota
                derrotes += 1
        for partit in lliga.partits.filter(equip_visitant=equip):
            gols_favor += partit.gols_visitant()
            gols_contra += partit.gols_local()
            if partit.gols_local() < partit.gols_visitant():
                # victoria
                victories += 1
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                # empate
                empats += 1
                punts += 1
            else:
                # derrota
                derrotes += 1
        classi.append( {"punts":punts, "equip":equip.nom,"victories":victories, "derrotes":derrotes, "empats":empats, "gols_local":gols_favor, "gols_visitant":gols_contra} )
    # ordenem llista
    classi.sort(key=lambda x: (x["punts"], x["gols_local"] / (x["gols_visitant"] or 1)), reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga.nom
                })
