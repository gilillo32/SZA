#!/usr/bin/env python3

import socket
import BerogailuLista
import komand_proz_funtzioak
from zerbitzari_errore import ErroreaEskaeran, ErrParamFormatuEzEgoki

PORT = 50001
EOF = "\n\r"

berogailuak = BerogailuLista.BerogailuLista()


def NOWkomandoa(berogailuak):
    if not parametroa:
        # berogailu bakoitzean dagoeen uneko hozberoa
        iterator = berogailuak.__iter__(berogailuak)
        erantzunaren_parte = ""
        while iterator.__next__(berogailuak) != None:
            berogailua = berogailuak.bilatuId(berogailuak, id)
            unekoHozberoa = berogailua.unekoHozberoaBueltatu()
            erantzunaren_parte += "$(unekoHozberoa)" + ":"
        erantzuna = ("+" + "$(erantzunaren_parte)").encode()
    else:  # parametroa sartu da
        try:
            id = int(parametroa.decode())
            berogailua = berogailuak.bilatuId(berogailuak, id)

            if berogailua == None:  # id hori duen berogailurik ez da existitzen
                errorea = '2'  # DUDAA--> ESTO BIEN???
                erantzuna = errorea.encode()
            else:  # existitzen da
                unekoHozberoa = berogailua.unekoHozberoaBueltatu()
                erantzuna = ("+" + "$(unekoHozberoa)").encode()

        except ValueError:
            # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
            errorea = "-4"
            erantzuna = errorea.encode()


def OFFkomandoa(id_berogailu):
    # TODO Iñigo
    berogailua = berogailuak.bilatuId(id_berogailu)
    berogailua.egoeraAldatu(False)

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
        erantzuna = "+"
    else:
        erantzuna = "-" + str(errorekodea)
    # TODO Kodetu behar da. Formatua ASCII-n egongo da hortaz UTF-8 Formatuan ere
    return erantzuna

def NAMkomandoa():
    errorekodea = 13
    erantzuna = ""
    egoeraEgokia = True

    berDeskribLista = []
    itrBerogailu = berogailuak.getIteradorea()
    for ber in itrBerogailu:
        bIzena = ber.getIzena()
        bID = ber.getId()
        berDeskrib = str(bIzena) + "," + str(bID)
        berDeskribLista.append(berDeskrib)
    erantzuna = berDeskribLista.join(":")

    if egoeraEgokia:
        erantzuna = "+" + erantzuna
    else:
        erantzuna = "-" + str(errorekodea)



    
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

    erantzuna = b''

    # sartutako komando bakoitzeko kasu bat
    if komandoa.case("ONN"):
        ONNkomandoa(parametroa)
    elif komandoa.case("OFF"):
        # OFFkomandoa(parametroa[##################   DUDA   ###############################################])
        pass
    elif komandoa.case("NAM"):
        pass
    elif komandoa.case("NOW"):
        pass
        NOWkomandoa(berogailuak)
    elif komandoa.case("GET"):
        pass
    elif komandoa.case("SET"):
        pass
    else:
        # komando ezezaguna
        errorea = "-1"
        erantzuna = errorea.encode()

    s.sendto(mezua, bez_helb)
# noinspection PyUnreachableCode
s.close()
