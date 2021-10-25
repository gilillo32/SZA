#!/usr/bin/env python3
import Berogailu
import random


class BerogailuLista(object):

    def __init__(self):
        self.lista = []

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
            # hasieratu piztuta edo itzalita egotea, uneko tenperatura eta desio tenperatura ausaz
            unekoTenp = round(random.uniform(0.0, 30.0), 1)
            desioTenp = round(random.uniform(0.0, 30.0), 1)
            piztuta = random.choice([True, False])
            berog = Berogailu.Berogailua(i, f"Gela {i}", unekoTenp, desioTenp, piztuta)
            self.lista.append(berog)

    def addBerogailua(self, berogailua):
        self.lista.append(berogailua)

    def copy(self):
        berogailuListaBerria = BerogailuLista()
        for berog in self.lista:
            berogailuListaBerria.addBerogailua(berog.copy())
        return berogailuListaBerria
