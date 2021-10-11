#!/usr/bin/env python3
import Berogailua

class BerogailuLista:
  def __init__(self):
    self.lista = []
    hasieratuBerogailuak()
  
  def bilatuId(self, id):
    for i in self.lista:
      if i.idBerdinaDu(id):
        return i
    return None

  def hasieratuBerogailuak(self):
    
