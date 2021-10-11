#!/usr/bin/env python3

import socket
import BerogailuLista

PORT = 50001

berogailuak = BerogailuLista.BerogailuLista()

#Sortu socketa eta esleitu helbide bat.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

while True:
	#Jaso mezu bat eta erantzun datu berdinekin.
	mezua, bez_helb = s.recvfrom(1024)
  komandoa = mezua[:3]
  
	s.sendto(mezua, bez_helb)
"""IKASLEAK BETETZEKO:
Itxi socketa.
"""
s.close()

