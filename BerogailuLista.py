#!/usr/bin/env python3
import Berogailu

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

  def hasieratuBerogailuak(self):
      
  
  def egoeraAldatuGuztiei(self, egoera):
    for berogailu in self.lista:
      berogailu.egoeraAldatu(egoera)

