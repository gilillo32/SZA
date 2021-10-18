#!/usr/bin/env python3

import socket
import BerogailuLista

PORT = 50001

berogailuak = BerogailuLista.BerogailuLista()


def NOWkomandoa():
    if not parametroa:
        # berogailu bakoitzean dagoeen uneko hozberoa
        iterator = berogailuak.__iter__()
        erantzunaren_parte = ""
        while iterator.__next__(berogailuak) != None:
            berogailua = berogailuak.bilatuId(id)
            unekoHozberoa = berogailua.unekoHozberoaBueltatu()
            erantzunaren_parte += "$(unekoHozberoa)" + ":"
        erantzuna = ("+" + "$(erantzunaren_parte)").encode()
    else:  # parametroa sartu da
        try:
            id = int(parametroa.decode())
            berogailua = berogailuak.bilatuId(id)

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

def GETkomandoa():
    if not parametroa:
        # berogailu bakoitzean dagoeen uneko hozberoa
        iterator = berogailuak.__iter__()
        erantzunaren_parte = ""
        while iterator.__next__(berogailuak) != None:
            berogailua = berogailuak.bilatuId(id)
            desioHozberoa = berogailua.desioHozberoaBueltatu()
            erantzunaren_parte += "$(desioHozberoa)" + ":"
        erantzuna = ("+" + "$(erantzunaren_parte)").encode()
    else:  # parametroa sartu da
        try:
            id = int(parametroa.decode())
            berogailua = berogailuak.bilatuId(id)

            if berogailua == None:  # id hori duen berogailurik ez da existitzen
                errorea = '2'  # DUDAA--> ESTO BIEN???
                erantzuna = errorea.encode()
            else:  # existitzen da
                desioHozberoa = berogailua.desioHozberoaBueltatu()
                erantzuna = ("+" + "$(desioHozberoa)").encode()

        except ValueError:
            # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
            errorea = "-4"
            erantzuna = errorea.encode()

def OFFkomandoa(id_berogailu):
    # TODO Iñigo
    berogailua = berogailuak.bilatuId(id_berogailu)
    berogailua.egoeraAldatu(False)


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
        pass
    elif komandoa.case("OFF"):
        # OFFkomandoa(parametroa[##################   DUDA   ###############################################])
        pass
    elif komandoa.case("NAM"):
        pass
    elif komandoa.case("NOW"):
        pass
        NOWkomandoa()
    elif komandoa.case("GET"):
        pass
        GETkomandoa()
    elif komandoa.case("SET"):
        pass
    else:
        # komando ezezaguna
        errorea = "-1"
        erantzuna = errorea.encode()

    s.sendto(mezua, bez_helb)
# noinspection PyUnreachableCode
s.close()
