#!/usr/bin/env python

import componentes
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
  #print('Caracter: ' + ch)
  if ch==" ":
    while ch == " ":
      ch = self.flujo.siguiente()
    self.flujo.devuelve(ch)
    return self.Analiza()
  elif ch== "+":
    return componentes.OpAdd("+", self.nlinea)     
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
      self.flujo.devuelve(newCh)
      return componentes.DosPtos()
  elif ch.isalpha():
    word = ""
    while ((ch).isalnum()):
      word += ch
      ch = self.flujo.siguiente()
    self.flujo.devuelve(ch)
    if word in self.PR:
      return componentes.PR(word, self.nlinea)
    else:
      return componentes.Identif(word, self.nlinea)
  elif ch.isdigit():
    num = ""
    num+=ch
    ch=self.flujo.siguiente()
    while(ch.isdigit()):
      num+=ch
      ch=self.flujo.siguiente()
    if (ch != '.'):
      self.flujo.devuelve(ch)
      return componentes.Numero(num, self.nlinea, 'ENTERO')
    else:
      newCh = self.flujo.siguiente()
      if not (newCh.isdigit()):
        self.flujo.devuelve(newCh)
        self.flujo.devuelve(ch)
        print "ERROR: NUMERO REAL MAL ESPECIFICADO" # tenemos un comentario no abierto
        return self.Analiza()
      num+=ch
      num+=newCh
      ch=self.flujo.siguiente()
      while((ch).isdigit()):
        num+=ch
        ch=self.flujo.siguiente()
      self.flujo.devuelve(ch)
      return componentes.Numero(num, self.nlinea, 'REAL')
  elif (ch is not '' and ord(ch) == 13):
    self.nlinea += 1
    return self.Analiza()
  elif (ch is not '' and ord(ch) == 10):
    self.nlinea += 1
    return self.Analiza()
  elif (ch is not '' and ord(ch) == 9):
    return self.Analiza()
  elif ch == '=':
    return componentes.OpRel('=', self.nlinea)
  elif ch == '<':
    newCh = self.flujo.siguiente()
    if newCh == '>':
      return componentes.OpRel('<>', self.nlinea)
    elif newCh == '=':
      return componentes.OpRel('<=', self.nlinea)
    else:
      self.flujo.devuelve(newCh)
      return componentes.OpRel('<', self.nlinea)
  elif ch == '>':
    newCh = self.flujo.siguiente()
    if newCh == '=':
      return componentes.OpRel('>=', self.nlinea)
    else:
      self.flujo.devuelve(newCh)
      return componentes.OpRel('>', self.nlinea)
  elif len(ch) is not 0:
    print "ERROR: CARACTER NO DEFINIDO EN LA ESPECIFICACION DEL LENGUAJE"
    return self.Analiza()
  else:
    return componentes.EOF()

    


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
    txt=open(filename).read()
    print "Este es tu fichero %r" % filename
    i=0
    fl = flujo.Flujo(txt)
    analex=Analex(fl)
    c=analex.Analiza()
    while c.cat != "EOF":
      print c
      c=analex.Analiza()
    print c
    

