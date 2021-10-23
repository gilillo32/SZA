#!/usr/bin/env python3
import socket
import BerogailuLista

PORT = 50001
MAX_BYTES_DATAGRAM = 1500

berogailuak = BerogailuLista.BerogailuLista()


def NOWGETkomandoa(aukera):
    """
    NOW eta GET komandoekin egiten dena berdina da, baina batek uneko tenperaturarekin
    egiten du eta besteak desio tenperaturarekin. Beraz, metodo orokor bat egingo dugu
    zeinak sartzen duzun aukeraren(NOW edo GET) arabera desio edo uneko tenperatura
    itzultzen duen.
    """
    if not parametroak:
        # berogailu bakoitzean dagoen uneko hozberoa
        iterator = berogailuak.getIteradorea()
        erantzunaren_parte = ""
        for ber in iterator:
            tenperatura = 0
            if aukera == "NOW":  # uneko hozberoa nahi dugu
                tenperatura = ber.unekoHozberoaBueltatu()
            elif aukera == "GET":  # desio hozberoa nahi dugu
                tenperatura = ber.desioHozberoaBueltatu()

            # bakarrik nahi dugu atal osoa eta gainera 3 zifrako zenbakia izango da koma kenduta eta tenperatua<10
            # bada 0 gehitu aurrean 3 zenbaki atal osoan lortu
            tenperatura *= 10
            # atal dezimala lortu
            tenperatura = int(tenperatura)
            # ikusi ea 3 zifrako zenbakia den, bestela 0 gehitu aurrean
            if len(str(tenperatura)) == 2:  # 0 gehitu ezkerrean
                erantzunaren_parte += "0" + str(int(tenperatura)) + ":"
            elif len(str(tenperatura)) == 1:  # 00 gehitu ezkerrean
                erantzunaren_parte += "00" + str(int(tenperatura)) + ":"
            else:
                erantzunaren_parte += str(int(tenperatura)) + ":"

        ema = ("+" + erantzunaren_parte[
                     0:len(erantzunaren_parte) - 1])  # ez dugu bueltatu behar azkenengo karakterea (:)
    else:  # parametroa sartu da
        try:
            # parametroa id-a dago
            berogailua = berogailuak.bilatuId(int(parametroak))
            if berogailua is None:  # id hori duen berogailurik ez da existitzen
                if aukera == "NOW":
                    ema = '-14'  # errorea 14 izango da
                elif aukera == "GET":
                    ema = '-15'  # errorea 15 izango da

            else:  # existitzen da
                tenperatura = 0
                if aukera == "NOW":  # uneko hozberoa nahi dugu
                    tenperatura = berogailua.unekoHozberoaBueltatu()
                elif aukera == "GET":  # desio hozberoa nahi dugu
                    tenperatura = berogailua.desioHozberoaBueltatu()

                # bakarrik nahi dugu atal osoa eta gainera 3 zifrako zenbakia izango da koma kenduta eta
                # tenperatua<10 bada 0 gehitu aurrean 3 zenbaki atal osoan lortu
                tenperatura *= 10
                # atal dezimala lortu
                tenperatura = int(tenperatura)
                # ikusi ea 3 zifrako zenbakia den, bestela 0 gehitu aurrean
                if len(str(tenperatura)) == 2:  # 0 gehitu ezkerrean
                    tenperatura = "0" + str(int(tenperatura))
                elif len(str(tenperatura)) == 1:  # 00 gehitu ezkerrean
                    tenperatura = "00" + str(int(tenperatura))
                ema = ("+" + str(tenperatura))

        except ValueError:
            # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
            ema = "-4"  # errore 4 itzuli
    return ema


def OFFkomandoa(id_berogailu):
    bueltan = '+'
    if not id_berogailu:
        for bg in berogailuak.getIteradorea():
            if bg.getEgoera():
                bg.egoeraAldatu(False)
    else:
        berogailua = berogailuak.bilatuId(int(id_berogailu))
        if berogailua is None:
            bueltan = '-12'
        else:
            berogailua.egoeraAldatu(False)
    return bueltan


def ONNkomandoa(id_berogailu):
    errorekodea = 0  # 0 bada ez dago errorerik oraindik
    if not id_berogailu:
        # Berogailu guztiak piztu: ez da parametrorik jaso
        berogailuak.egoeraAldatuGuztiei(True)
    else:
        # Frogaketak:
        try:  # Jaso den parametroa zenbaki bat den frogatu (ID bat izango da eta)
            id_zenb = int(id_berogailu)
            if id_zenb < 0:  # Jasotako zenbakia ez da negatiboa
                raise ValueError()
        except ValueError:
            errorekodea = 4  # Formatu errorea: Jasotako parametroa ez da zenbaki bat edo zenbaki negatiboa da

        if not errorekodea:
            unek = berogailuak.bilatuId(id_zenb)
            if unek is not None:
                # ID- hori duen berogailua piztu
                unek.egoeraAldatu(True)
            else:
                # Ezin da eragiketa burutu
                errorekodea = 11  # Err ONN. Ez dago '{id_zenb}' ID-a duen berogailurik

    if not errorekodea:
        bueltan = "+"
    else:
        bueltan = "-" + str(errorekodea)
    return bueltan


def NAMkomandoa(parametroak):
    errorekodea = 0 # 0 bada ez dago errorerik oraindik

    # Berogailuen deskribapenak ("ID,izena" tuplak) gordeko diren array-a hasieratu
    berogdeskriblista = []
    # Berogailu bakoitza iteratzeko, berogailu listari iteradore bat eskatu eta aldagai batean gorde
    itrberogailu = berogailuak.getIteradorea()
    if not parametroak:
        try:
            for ber in itrberogailu: # Berogailu bakoitzeko
                # Uneko berogailuaren deskribapena lortzeko informazioa prestatu (ID eta Izena)
                bID = ber.getID()
                bIzena = ber.getIzena()
                # Uneko berogailuaren deskribapena sortu (ID,Izena)
                berDeskrib = str(bID) + "," + str(bIzena)
                # Uneko berogailuaren deskribapena berogailu deskribapen listari gehitu
                berogdeskriblista.append(berDeskrib)
            # Berogailu deskribapen listako elmentu guztiak ":" karakterearekin konkatenatu
            bueltan = ":".join(berogdeskriblista)
        except Exception:
            # Datuen bilketan edo prozezaketan errore bat egon bada, orduan egoera ez egokia dela adierazi
            errorekodea = 13
    else:
        errorekodea = 2 # NAM komandoak parametroak jaso ditu eta ez luke parametrorik jaso beharko.

    if not errorekodea:
        # Bidaliko den mezua prestatu
        bueltan = "+" + bueltan

        # Bidaliko den mezua luzeera maximoa gainditzen ez duela frogatu eta gainditzen badu murriztu
        bueltan = __zerrendaLuzeeraMaxEzGainditu(bueltan)

    else:
        # Egoera ez egokia: Errorea mezuaren exekuzioan gertatu da, errore mezua prestatu
        bueltan = "-" + str(errorekodea)
    return bueltan

def __zerrendaLuzeeraMaxEzGainditu(zerrenda):
    bueltaZerrenda = zerrenda
    # Bidaliko den mezua luzeera maximoa gainditzen ez duela frogatu eta gainditzen badu murriztu
    if len(bueltaZerrenda.encode()) > MAX_BYTES_DATAGRAM:
        # DATAGRAMA BYTE LUZEERA MAXIMOA GAINDITU DA: {MAX_BYTES_DATAGRAM}
        # Mezuaren luzeera txikituko da informazioa borratuz
        bueltanBytes = bytearray(
            bueltaZerrenda.encode())  # byteko lehenengo MAX_BYTES_DATAGRAM kopurua lortzeko byte array bat sortu
        bueltanBytes = bueltanBytes[
                       :MAX_BYTES_DATAGRAM]  # bytearrayko lehenengo MAX_BYTES_DATAGRAM elementuak lortu
        bueltaZerrenda = bueltanBytes.decode("utf-8",
                                      "ignore")  # saiatu zatituko mezua dekodetzen eta byte-ren bat ezin bada
        # dekodetu (adb: zatiketak karaktere baten definizioa zatitu du) byte hori ignoratu
        bueltaZerrenda = bueltaZerrenda.rsplit(':', 1)[0]  # azkenengo ":" karakterearen ondoren dagoen informazioa baztertu
    return bueltaZerrenda


def SETkomandoa(param):
    if not param:
        return '-3'
    else:
        tenp = param[:3]
        bg_id = param[3:]
        egoeraEgokia = True
        try:
            tenp = int(tenp)
            if tenp < 0:
                raise ValueError()
        except ValueError:  # Hozberoa zenbaki osoa izan behar da
            return '-4'
        if not bg_id:
            for bg in berogailuak.getIteradorea():
                bg.setDesioTenp(tenp)
        else:
            bg = berogailuak.bilatuId(bg_id)
            if not bg:
                return '-16'
            bg.setDesioTenp(tenp)
        if not egoeraEgokia:
            return '-16'



# Sortu socketa eta esleitu helbide bat.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

while True:
    # Jaso mezu bat eta erantzun datu berdinekin.
    mezua, bez_helb = s.recvfrom(1024)
    # Jasotako mezua ASCII formatuan dekodetu
    mezua = mezua.decode("ascii")
    # komandoak 3 parametro izango dituzte
    komandoa = mezua[:3]
    # parametroak (izatekotan) komandoen atzetik doaz
    parametroak = mezua[3:]
    # Erantzuna hasieratu
    erantzuna = ''

    # sartutako komando bakoitzeko kasu bat
    if komandoa == "ONN":
        erantzuna = ONNkomandoa(parametroak).encode("ascii")
    elif komandoa == "OFF":
        erantzuna = OFFkomandoa(parametroak).encode("ascii")
    elif komandoa == "NAM":
        erantzuna = NAMkomandoa(parametroak).encode("utf-8")
    elif komandoa == "NOW":
        erantzuna = NOWGETkomandoa("NOW").encode("ascii")
    elif komandoa == "GET":
        erantzuna = NOWGETkomandoa("GET").encode("ascii")
    elif komandoa == "SET":
        erantzuna = SETkomandoa(parametroak).encode("ascii")
    else:
        # komando ezezaguna
        erantzuna = "-1".encode("ascii")  # errorea

    s.sendto(erantzuna, bez_helb)
# noinspection PyUnreachableCode
s.close()
