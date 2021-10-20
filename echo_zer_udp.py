#!/usr/bin/env python3
import math
import socket
import BerogailuLista

PORT = 50001
EOF = "\n\r"

berogailuak = BerogailuLista.BerogailuLista()
berogailuak.hasieratuBerogailuak()


def NOWkomandoa():
	if not parametroak:
			# berogailu bakoitzean dagoen uneko hozberoa
			iterator = berogailuak.getIteradorea()
			erantzunaren_parte = ""
			for ber in iterator:
			unekoHozberoa = ber.unekoHozberoaBueltatu()
			#bakarrik nahi dugu atal osoa eta gainera 3 zifrako zenbakia izango da koma kenduta eta tenperatua<10 bada 0 gehitu aurrean
			#3 zenbaki atal osoan lortu
			unekoHozberoa *= 10
			#atal dezimala lortu
			unekoHozberoa = int(unekoHozberoa)
			#ikusi ea 3 zifrako zenbakia den, bestela 0 gehitu aurrean
			if len(str(unekoHozberoa)) == 2: #0 gehitu ezkerrean
				erantzunaren_parte += str(0)+ str(int(unekoHozberoa)) + ":"
			elif len(str(unekoHozberoa)) == 1: #00 gehitu ezkerrean
				erantzunaren_parte += str(00)+ str(int(unekoHozberoa)) + ":"
			else:
				erantzunaren_parte += str(int(unekoHozberoa)) + ":"

			ema = ("+" + erantzunaren_parte[0:len(erantzunaren_parte)-1]) #ez dugu bueltatu behar azkenengo karakterea (:)
	else:  # parametroa sartu da
		try:
			id = int(parametroak.decode())
			berogailua = berogailuak.bilatuId(id)
			if berogailua == None:  # id hori duen berogailurik ez da existitzen
				ema = '-14'  # errorea 14 izango da
			else:  # existitzen da
					unekoHozberoa = berogailua.unekoHozberoaBueltatu()
				#bakarrik nahi dugu atal osoa eta gainera 3 zifrako zenbakia izango da koma kenduta eta tenperatua<10 bada 0 gehitu aurrean
				#3 zenbaki atal osoan lortu
					unekoHozberoa *= 10
				#atal dezimala lortu
					unekoHozberoa = int(unekoHozberoa)
					#ikusi ea 3 zifrako zenbakia den, bestela 0 gehitu aurrean
					if len(str(unekoHozberoa)) == 2: #0-ak gehitu ezkerrean
						unekoHozberoa= str(0)+ str(int(unekoHozberoa))
					elif len(str(unekoHozberoa)) == 1: #00 gehitu ezkerrean
						unekoHozberoa = str(00)+ str(int(unekoHozberoa))
					ema = ( "+" + str(unekoHozberoa))

		except ValueError:
			# kasting-a ezin bada egin string bat delako--> parametroak ez du forma egokia
			ema = "-4"  # errore 4 itzuli
	return ema


def GETkomandoa():
	if not parametroak:
		# berogailu bakoitzean dagoeen uneko hozberoa
		iterator = berogailuak.getIteradorea()
		erantzunaren_parte = ""
		for ber in iterator:
			berogailua = ber.bilatuId(id)
			desioHozberoa = ber.desioHozberoaBueltatu()
			erantzunaren_parte += desioHozberoa + ":"
		ema = "+" + erantzunaren_parte
	else:  # parametroa sartu da
		try:
			id = int(parametroak.decode())
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
	berogailua = berogailuak.bilatuId(id_berogailu)
	berogailua.egoeraAldatu(False)
	bueltan = '+'
	if not id_berogailu:
		for bg in berogailuak:
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
			errorekodea = 4  # Formatu errorea: Jasotako parametroa ez da zenbaki bat
			egoeraEgokia = False
		if egoeraEgokia and id_zenb < 0:
			errorekodea = 4  # Formatu errorea: Jasotako parametroa negatiboa da
			egoeraEgokia = False

		if egoeraEgokia:
			unek = berogailuak.bilatuId(id_zenb)
			if unek != None:
				# ID- hori duen berogailua piztu
				unek.egoeraAldatu(True)
			else:
				# Ezin da eragiketa burutu
				errorekodea = 11  # Err ONN. Ez dago '{id_zenb}' ID-a duen berogailurik
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


def SETkomandoa(param):
	if not param:
		return '-3'
	else:
		tenp = param[:3]
		bg_id = param[3:]
		egoeraEgokia = True
		try:
			tenp = int(tenp)
		except ValueError:  # Hozberoa zenbaki osoa izan behar da
			return '-4'
		if not bg_id:
			for bg in berogailuak.getIteradorea():
				bg.setDesioTenp(tenp)
		else:
			bg = berogailuak.bilatuId(bg_id)
			bg.setDesioTenp(tenp)
		if not egoeraEgokia:
			return '-16'

# Sortu socketa eta esleitu helbide bat.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

while True:
	# Jaso mezu bat eta erantzun datu berdinekin.
	mezua, bez_helb = s.recvfrom(1024)
	mezua = mezua.decode()
	# komandoak 3 parametro izango dituzte
	komandoa = mezua[:3]
	print(komandoa)
	# parametroak(izatekotan) komandoen atzetik doaz
	parametroak = mezua[3:]
	print(parametroak)
	erantzuna = ''

	# sartutako komando bakoitzeko kasu bat
	if komandoa == "ONN":
		erantzuna = ONNkomandoa(parametroak)
	elif komandoa == "OFF":
		erantzuna = OFFkomandoa(parametroak)
	elif komandoa == "NAM":
		erantzuna = NAMkomandoa()
	elif komandoa == "NOW":
		erantzuna = NOWkomandoa()
	elif komandoa == "GET":
		erantzuna = GETkomandoa()
	elif komandoa =="SET":
		erantzuna = SETkomandoa(parametroak)
	else:
		# komando ezezaguna
		erantzuna = "-1"  # errorea

	print(erantzuna)
	s.sendto(erantzuna.encode(), bez_helb)
# noinspection PyUnreachableCode
s.close()