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
    if isinstance(piztuta, types.BooleanType):
      self.__piztuta = piztuta
    else:
      print("\nTrue/False idatzi behar da azkeneko parametroa.\n")

  def egoeraAldatu(self, egoera):
    self.__piztuta = egoera

  def idBerdinaDu(self, id):
    return id == self.id
  
  def unekoHozberoaBueltatu(self):
    return self.__uneko_tenp

  def desioHozberoaBueltatu(self):
    return self.__desio_tenp

  def getID(self):
    return  self.__id

  def getIzena(self):
    return self.__izena


