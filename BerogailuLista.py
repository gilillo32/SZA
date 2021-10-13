#!/usr/bin/env python3
import Berogailua

class BerogailuLista:
  def __init__(self):
    self.pos
    self.lista = []
    self.hasieratuBerogailuak()
  
  def bilatuId(self, id):
    for i in self.lista:
      if i.idBerdinaDu(id):
        return i
    return None

  def __iter__(self):
    self.pos = 0
    return self

  def __next__(self):
    if self.pos == len(self.lista):
      return None
    else:
      x = self.lista[self.pos]
      self.pos += 1
      return x

  def hasieratuBerogailuak(self):
    
