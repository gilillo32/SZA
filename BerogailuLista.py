#!/usr/bin/env python3
import Berogailu
import random

class BerogailuLista(object):

    def __init__(self):
        self.pos
        self.lista = []
        self.hasieratuBerogailuak()

    def bilatuId(self, id):
        for i in self.lista:
            if i.idBerdinaDu(id):
                return i
        return None

    def getIteradorea(self):
        return iter(self.lista)

    def egoeraAldatuGuztiei(self, egoera):
        for berogailu in self.lista:
            berogailu.egoeraAldatu(egoera)

    def hasieratuBerogailuak(self):
        berogailuKop = 10
        for i in range(1, berogailuKop + 1):
          #hasieratu piztuta edo itzalita egotea, uneko tenperatura eta desio tenperatura ausaz
            unekoTenp = random.uniform(-20.0, 30.0)
            desioTenp = random.uniform(-20.0, 30.0)
            piztuta = random.choice([True, False])
            self.lista.append(Berogailu.Berogailua(i, f"Gela {i}",unekoTenp,desioTenp,piztuta))
            
