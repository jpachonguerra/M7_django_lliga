from django.shortcuts import render

from futbol.models import *

# Create your views here.

def classificacio(request):
    lliga = Lliga.objects.all()[1]
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
