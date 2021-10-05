#!/usr/bin/env python3

import socket

PORT = 50001

"""IKASLEAK BETETZEKO:
Sortu socketa eta esleitu helbide bat.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

while True:
	"""IKASLEAK BETETZEKO:
	Jaso mezu bat eta erantzun datu berdinekin.
	"""
	mezua, bez_helb = s.recvfrom(1024)
	s.sendto(mezua, bez_helb)
"""IKASLEAK BETETZEKO:
Itxi socketa.
"""
s.close()

