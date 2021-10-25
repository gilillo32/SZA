#!/usr/bin/env python3

import types

import Berogailu


class Berogailua:
  
  def __init__(self, id, izena, uneko_tenp = 0.0, desio_tenp = 0.0, piztuta = False):
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
    return id == self.__id

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
    self.__uneko_tenp = self.__desio_tenp

  def copy(self):
    berogailuBerria = Berogailu.Berogailua(self.__id, self.__izena, self.__uneko_tenp,
                                           self.__desio_tenp, self.__piztuta)
    return berogailuBerria
