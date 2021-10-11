#!/usr/bin/env python3

class Berogailua:
  
  def __init__(self, id, izena, Utenperatura = 0, Dtenperatura = 0, piztuta = False):
    self.__id = id
    self.__izena = izena
    self.__uneko_temp = Utenperatura
    self.__desio_temo = Dtenperatura
    self.__piztuta = piztuta

  def egoeraAldatu(self, egoera):
    self.__piztuta = egoera

  def idBerdinaDu(self, id):
    return id = self.id



