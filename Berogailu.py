#!/usr/bin/env python3

import types

class Berogailua:
  
  def __init__(self, id, izena, uneko_tenp = 0, desio_tenp = 0, piztuta = False):
    try:
      self.__id = int(id)
    except ValueError:
      print("\nID ez-egokia sartu duzu.\n")
    self.__izena = izena
    self.__uneko_tenp = uneko_tenp
    self.__desio_tenp = desio_tenp
    if isinstance(piztuta, bool):
      self.__piztuta = piztuta
    else:
      print("\nTrue/False idatzi behar da azkeneko parametroa.\n")

  def egoeraAldatu(self, egoera):
    self.__piztuta = egoera

  def getEgoera(self):
    return self.__piztuta

  def idBerdinaDu(self, id):
    return id == self.id

  def unekoHozberoaBueltatu(self):
    return self.__uneko_tenp

  def desioHozberoaBueltatu(self):
    return self.__desio_tenp

  def getID(self):
    return self.__id

  def getIzena(self):
    return self.__izena

  def setDesioTenp(self, tenp):
    self.__desio_tenp = tenp
    self.tenpLortu()

  def tenpLortu(self):
    print("\nDesio den hozberora iristen...\n")
    self.__uneko_tenp = self.__desio_tenp
    print("\nDesio zen hozberora iritsi da\n")


