#!/usr/bin/env python3
import socket
import BerogailuLista
from zerbitzari_errore import ErroreaEskaeran, ErrParamFormatuEzEgoki, ErrEzEsperoParam, ErrHautaParamFalta, \
    ErrKomandoEzezaguna

PORT = 50001
MAX_BYTES_DATAGRAM = 1500

berogailuak = BerogailuLista.BerogailuLista()

def NOWGETkomandoa(aukera, parametroak):
    """
    NOW eta GET komandoekin egiten dena berdina da, baina batek uneko tenperaturarekin
    egiten du eta besteak desio tenperaturarekin. Beraz, metodo orokor bat egingo dugu
    zeinak sartzen duzun aukeraren(NOW edo GET) arabera desio edo uneko tenperatura
    itzultzen duen.
    :param parametroak:
    """
    if not parametroak:
        ema = __NOWGETkomandoaParamEz(aukera)
    else:  # parametroa sartu da
        ema = __NOWGETkomandoaParamBai(aukera, parametroak)
    return __zerrendaLuzeeraMaxEzGainditu(ema)


def __NOWGETkomandoaParamEz(aukera):
    # berogailu bakoitzean dagoen uneko hozberoa
    iterator = berogailuak.getIteradorea()
    erantzunaren_parte = ""
    for ber in iterator:
        tenperatura = 0
        if aukera == "NOW":  # uneko hozberoa nahi dugu
            tenperatura = ber.unekoHozberoaBueltatu()
        elif aukera == "GET":  # desio hozberoa nahi dugu
            tenperatura = ber.desioHozberoaBueltatu()

        erantzunaren_parte += __parseTenperatura(tenperatura) + ":"
    ema = ("+" + erantzunaren_parte[
                 0:len(erantzunaren_parte) - 1])  # ez dugu bueltatu behar azkenengo karakterea (:)
    return ema


def __NOWGETkomandoaParamBai(aukera, parametroak):
    try:
        # parametroa id-a dago
        berogailua = berogailuak.bilatuId(int(parametroak))
        if berogailua is None:  # id hori duen berogailurik ez da existitzen
            if aukera == "NOW":
                raise ErroreaEskaeran(14)  # errorea 14 izango da
            elif aukera == "GET":
                raise ErroreaEskaeran(15)  # errorea 15 izango da

        else:  # existitzen da
            tenperatura = 0
            if aukera == "NOW":  # uneko hozberoa nahi dugu
                tenperatura = berogailua.unekoHozberoaBueltatu()
            elif aukera == "GET":  # desio hozberoa nahi dugu
                tenperatura = berogailua.desioHozberoaBueltatu()

            ema = "+" + __parseTenperatura(tenperatura)

    except ValueError:
        # kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
        raise ErrParamFormatuEzEgoki()  # errore 4 itzuli
    return ema


def __parseTenperatura(tenperatura):
    # bakarrik nahi dugu atal osoa eta gainera 3 zifrako zenbakia izango da koma kenduta eta
    # tenperatua<10 bada 0 gehitu aurrean 3 zenbaki atal osoan lortu
    tenperatura *= 10
    # atal dezimala lortu
    tenperatura = int(tenperatura)
    # ikusi ea 3 zifrako zenbakia den, bestela 0 gehitu aurrean
    if len(str(tenperatura)) == 2:  # 0 gehitu ezkerrean
        tenperatura = "0" + str(tenperatura)
    elif len(str(tenperatura)) == 1:  # 00 gehitu ezkerrean
        tenperatura = "00" + str(tenperatura)
    ema = str(tenperatura)
    return ema


def OFFkomandoa(id_berogailu):
    try:
        bueltan = __berogailuEgoeraAldatu(id_berogailu, False)
    except ErroreaEskaeran:
        raise ErroreaEskaeran(12) # Err OFF. Ez dago ID hori duen berogailurik

    return bueltan


def ONNkomandoa(id_berogailu):
    try:
        bueltan = __berogailuEgoeraAldatu(id_berogailu, True)
    except ErroreaEskaeran:
        raise ErroreaEskaeran(11) # Err ONN. Ez dago ID hori duen berogailurik

    return bueltan

def __berogailuEgoeraAldatu(id_berogailu, egoera):
    if not id_berogailu:
        # Berogailu guztiei egoera aldatu: ez da parametrorik jaso
        berogailuak.egoeraAldatuGuztiei(egoera)
    else:
        # Frogaketak:
        try:  # Jaso den parametroa zenbaki bat den frogatu (ID bat izango da eta)
            id_zenb = __toIntEtaPositiboa(id_berogailu)
        except ValueError:
            raise ErrParamFormatuEzEgoki()  # Formatu errorea: Jasotako parametroa ez da zenbaki bat edo zenbaki negatiboa da

        unek = berogailuak.bilatuId(id_zenb)
        if unek is not None:
            # ID- hori duen berogailuari egoera aldatu
            unek.egoeraAldatu(egoera)
        else:
            # Ezin da eragiketa burutu
            raise ErroreaEskaeran()

    bueltan = "+"
    return bueltan



def NAMkomandoa(parametroak):
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
            raise ErroreaEskaeran(13)
    else:
        raise ErrEzEsperoParam() # NAM komandoak parametroak jaso ditu eta ez luke parametrorik jaso beharko.


    bueltan = "+" + bueltan
    # Bidaliko den mezua luzeera maximoa gainditzen ez duela frogatu eta gainditzen badu murriztu
    bueltan = __zerrendaLuzeeraMaxEzGainditu(bueltan)


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
        raise ErrHautaParamFalta()

    tenp = param[:3]
    try:
        tenp = __toIntEtaPositiboa(tenp)
        tenp = tenp / 10
    except ValueError:  # Hozberoa zenbaki osoa izan behar da
        raise ErrParamFormatuEzEgoki()

    bg_id = param[4:]
    if not bg_id:
        for bg in berogailuak.getIteradorea():
            bg.setDesioTenp(tenp)
    else:
        try:
            bg_id = __toIntEtaPositiboa(bg_id)
        except ValueError:  # Hozberoa zenbaki osoa izan behar da
            raise ErrParamFormatuEzEgoki()

        bg = berogailuak.bilatuId(bg_id)
        if not bg:
            raise ErroreaEskaeran(16)
        bg.setDesioTenp(tenp)

    return "+"

"""
sartutako balioa zenbaki positiboa den ala ez frogatzen du.
Baldintzak betetzen baditu, zenbakia bueltatzen du int formatuan.
Baldintzak betetzen ez baditu, orduan ValueError salbuespena jaurtiko du
"""
def __toIntEtaPositiboa(balioa):
    ema = int(balioa)
    if ema < 0:
        raise ValueError()
    return ema


def main():
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
        try:
            # sartutako komando bakoitzeko kasu bat
            if komandoa == "ONN":
                erantzuna = ONNkomandoa(parametroak).encode("ascii")
            elif komandoa == "OFF":
                erantzuna = OFFkomandoa(parametroak).encode("ascii")
            elif komandoa == "NAM":
                erantzuna = NAMkomandoa(parametroak).encode("utf-8")
            elif komandoa == "NOW":
                erantzuna = NOWGETkomandoa("NOW", parametroak).encode("ascii")
            elif komandoa == "GET":
                erantzuna = NOWGETkomandoa("GET", parametroak).encode("ascii")
            elif komandoa == "SET":
                erantzuna = SETkomandoa(parametroak).encode("ascii")
            else:
                raise ErrKomandoEzezaguna() # komando ezezaguna
        except ErroreaEskaeran as errEsk:
            erantzuna = "-" + str(errEsk.get_errore_kode())
            erantzuna = erantzuna.encode("ascii")

        s.sendto(erantzuna, bez_helb)
    # noinspection PyUnreachableCode
    s.close()

# Programa hau explizituki exekutatzen bada, hau da, ez da inportatzen adibidez:
if __name__ == '__main__':
    # Programa nagusia exekutatu
    main()
