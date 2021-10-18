#!/usr/bin/env python3

import socket
import BerogailuLista

PORT = 50001
EOF = "\n\r"

berogailuak = BerogailuLista.BerogailuLista()
berogailuak.hasieratuBerogailuak()

def NOWkomandoa(berogailuak):
    if not parametroa:
        # berogailu bakoitzean dagoeen uneko hozberoa
        iterator = berogailuak.__iter__(berogailuak)
        erantzunaren_parte = ""
        while iterator.__next__(berogailuak) != None:
            berogailua = berogailuak.bilatuId(berogailuak, id)
            unekoHozberoa = berogailua.unekoHozberoaBueltatu()
            erantzunaren_parte += unekoHozberoa + ":"
        ema = ("+" + erantzunaren_parte)
    else:  # parametroa sartu da
        try:
            id = int(parametroa.decode())
            berogailua = berogailuak.bilatuId(berogailuak, id)

            if berogailua == None:  # id hori duen berogailurik ez da existitzen
                ema = '-14' #errorea 14 izango da            
            else:  # existitzen da
                unekoHozberoa = berogailua.unekoHozberoaBueltatu()
                ema = ("+" + unekoHozberoa)

        except ValueError:
            # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
            ema = "-4" #errore 4 itzuli
    return ema

def GETkomandoa():
    if not parametroa:
        # berogailu bakoitzean dagoeen uneko hozberoa
        iterator = berogailuak.__iter__()
        erantzunaren_parte = ""
        while iterator.__next__(berogailuak) != None:
            berogailua = berogailuak.bilatuId(id)
            desioHozberoa = berogailua.desioHozberoaBueltatu()
            erantzunaren_parte += desioHozberoa + ":"
        ema = "+" + erantzunaren_parte
    else:  # parametroa sartu da
        try:
            id = int(parametroa.decode())
            berogailua = berogailuak.bilatuId(id)

            if berogailua == None:  # id hori duen berogailurik ez da existitzen
                ema = '-15' 
            else:  # existitzen da
                desioHozberoa = berogailua.desioHozberoaBueltatu()
                ema = "+" + desioHozberoa

        except ValueError:
            # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
            ema = "-4"
    return ema
            
def OFFkomandoa(id_berogailu):
    # TODO Iñigo
    berogailua = berogailuak.bilatuId(id_berogailu)
    berogailua.egoeraAldatu(False)
    bueltan = '+'
    if not id_berogailu:
        for bg in berogailuak: #TODO getLista()
            if bg.getEgoera():
                bg.egoeraAldatu(False)
    else:
        berogailua = berogailuak.bilatuId(id_berogailu)
        if berogailua == None:
            bueltan = '-12'
        else:
            berogailua.egoeraAldatu(False)
    return bueltan

def ONNkomandoa(id_berogailu):
    errorekodea = 11
    egoeraEgokia = True
    if not id_berogailu:
        # Berogailu guztiak piztu: ez da parametrorik jaso
        berogailuak.aldatuEgoeraGuztiei(True)
    else:
        try:  # Jaso den parametroa zenbaki bat den frogatu (ID bat izango da eta)
            id_zenb = int(id_berogailu)
        except ValueError:
            errorekodea = 4 # Formatu errorea: Jasotako parametroa ez da zenbaki bat
            egoeraEgokia = False
        if egoeraEgokia and id_zenb < 0:
            errorekodea = 4 # Formatu errorea: Jasotako parametroa negatiboa da
            egoeraEgokia = False

        if egoeraEgokia:
            unek = berogailuak.bilatuId(id_zenb)
            if unek != None:
                # ID- hori duen berogailua piztu
                unek.egoeraAldatu(True)
            else:
                # Ezin da eragiketa burutu
                errorekodea = 11 # Err ONN. Ez dago '{id_zenb}' ID-a duen berogailurik
                egoeraEgokia = False

    if egoeraEgokia:
        bueltan = "+"
    else:
        bueltan = "-" + str(errorekodea)
    # TODO Kodetu behar da. Formatua ASCII-n egongo da hortaz UTF-8 Formatuan ere
    return bueltan

def NAMkomandoa():
    errorekodea = 13
    egoeraegokia = True

    berogdeskriblista = []
    itrberogailu = berogailuak.getIteradorea()
    for ber in itrberogailu:
        bIzena = ber.getIzena()
        bID = ber.getId()
        berDeskrib = str(bID) + "," + str(bIzena)
        berogdeskriblista.append(berDeskrib)
    bueltan = berogdeskriblista.join(":")

    if egoeraegokia:
        bueltan = "+" + bueltan
    else:
        bueltan = "-" + str(errorekodea)
    return bueltan

    
# Sortu socketa eta esleitu helbide bat.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

while True:
    # Jaso mezu bat eta erantzun datu berdinekin.
    mezua, bez_helb = s.recvfrom(1024)

    # komandoak 3 parametro izango dituzte
    komandoa = mezua[:3]

    # parametroak(izatekotan) komandoen atzetik doaz
    parametroa = mezua[3:]

    erantzuna = ''

    # sartutako komando bakoitzeko kasu bat
    if komandoa.case("ONN"):
        erantzuna = ONNkomandoa(parametroa)
    elif komandoa.case("OFF"):
        erantzuna = OFFkomandoa(parametroa)
    elif komandoa.case("NAM"):
        erantzuna = NAMkomandoa()
    elif komandoa.case("NOW"):
        erantzuna = NOWkomandoa()
    elif komandoa.case("GET"):
        erantzuna = GETkomandoa()
    elif komandoa.case("SET"):
        pass
    else:
        # komando ezezaguna
        erantzuna = "-1" #errorea

    s.sendto(erantzuna.encode(), bez_helb)
# noinspection PyUnreachableCode
s.close()
