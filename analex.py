#!/usr/bin/env python

import componentes
import errores
import flujo
import string
import sys

from sys import argv
from sets import ImmutableSet

class Analex:
#############################################################################
##  Conjunto de palabras reservadas para comprobar si un identificador es PR
#############################################################################
 PR = ImmutableSet(["PROGRAMA", "VAR", "VECTOR","DE", "ENTERO", "REAL", "BOOLEANO", "INICIO", "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO","FALSO"])

 ############################################################################
 #
 #  Funcion: __init__
 #  Tarea:  Constructor de la clase
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
 def __init__(self, flujo):
    #Debe completarse con  los campos de la clase que se consideren necesarios

    self.nlinea=1 #contador de lineas para identificar errores
    self.flujo = flujo

 ############################################################################
 #
 #  Funcion: Analiza
 #  Tarea:  Identifica los diferentes componentes lexicos
 #  Prametros:  --
 #  Devuelve: Devuelve un componente lexico
 #
 ############################################################################
 def Analiza(self):
  
  ch=self.flujo.siguiente()
  if ch==" ":
    while ch == " ":
      ch = self.flujo.siguiente()
    return self.Analiza(self.flujo)
  elif ch== "+":
    return OpAdd("+", self.nlinea)     
  elif ch== "-":
    return componentes.OpAdd("-",self.nlinea)
  elif ch== "*":
    return componentes.OpMult("*",self.nlinea)
  elif ch== "/":
    return componentes.OpMult("/",self.nlinea)
  elif ch== "(":
    return componentes.ParentAp()
  elif ch== ")":
    return componentes.ParentCi()
  elif ch== "[":
    return componentes.CorAp()
  elif ch== "]":
    return componentes.CorCi()
  elif ch== ".":
    return componentes.Punto()
  elif ch== ",":
    return componentes.Coma()
  elif ch== ";":
    return componentes.PtoComa()

  elif ch == "{":
    while ch != "}":
      ch = self.flujo.siguiente()
    return self.Analiza()
  elif ch == "}":
    print "ERROR: Comentario no abierto" # tenemos un comentario no abierto
    return self.Analiza()
  elif ch==":":
    newCh = self.flujo.siguiente()
    if newCh == "=":
      return componentes.OpAsigna()
    else:
      self.flujo.devolver(newCh)
      return componentes.DosPtos()
  elif ch.isalpha():
    word = []
    word.append(ch)
    #Python no se come estos iguales
    while ((ch = self.flujo.siguiente()).isalnum):
      word.append(ch)
    self.flujo.devolver(ch)
    if word in self.PR:
      return componentes.PR(word, self.nlinea)
    else:
      return componentes.Identif(word, self.nlinea)
  elif ch.isdigit():
    num = []
    num.append(ch)
    #Python no se come estos iguales
    while((ch=self.flujo.siguiente()).isdigit()):
      num.append(ch)
    if (ch != '.'):
      self.flujo.devolver(ch)
      return componentes.Numero(num, self.nlinea, 'INTEGER')
    else:
          #Python no se come estos iguales

      if not (newCh = self.flujo.siguiente().isdigit()):
        self.flujo.devolver(newCh)
        self.flujo.devolver(ch)
        print "ERROR: NUMERO REAL MAL ESPECIFICADO" # tenemos un comentario no abierto
        return self.Analiza()
      num.append(ch)
          #Python no se come estos iguales

      while((ch=self.flujo.siguiente()).isdigit()):
        num.append(ch)
      self.flujo.devolver(ch)
      return componentes.Numero(num, self.nlinea, 'FLOAT')
  elif ch== "\n":
    self.nlinea += 1
    self.Analiza()
    


############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__=="__main__":
    script, filename=argv
    txt=open(filename)
    print "Este es tu fichero %r" % filename
    i=0
    fl = flujo.Flujo(txt)
    analex=Analex(fl)
    try:
      c=analex.Analiza()
      while c :
       print c
       c=analex.Analiza()
      i=i+1
    except errores.Error, err:
     sys.stderr.write("%s\n" % err)
     analex.muestraError(sys.stderr)

