#!/usr/bin/env python

import componentes
import flujo
import string
import sys
import analex

from sys import argv
from sets import ImmutableSet

class Anasint:
    def __init__(self, lexico):
	self.tablaSim = {}
        self.lexico = lexico
        self.avanza()
        self.analizaPrograma()
        self.componente = None
    
    def avanza(self):
        self.componente = self.lexico.Analiza()
    
    def comprueba(self, cat):
        if self.componente.cat == cat:
            self.avanza()
        else: 
            print "Error: se esperaba " + cat
    
    def analizaPrograma(self):
        if self.componente.cat == "PR" and self.componente.valor == "PROGRAMA":
            self.avanza()
            self.comprueba("Identif")
            self.comprueba("PtoComa")
            self.analizaDeclVar()
            self.analizaInstrucciones()
            self.comprueba("Punto")
        else:
            print "Error: SE ESPERABA PR PROGRAMA en linea " + str(self.lexico.nlinea)
    
    def analizaDeclVar(self):
        if self.componente.cat == "PR" and self.componente.valor == "VAR":
            self.avanza()
            listaIDs = self.analizaListaId()
            self.comprueba("DosPtos")
            tipo = self.analizaTipo()
            self.comprueba("PtoComa")

	    # RESTRICCION SEMANTICA: No puede haber identificadores repetidos
	    for identif in listaIDs:
		if (identif in self.tablaSim):
		    print "Error: no puede haber identificadores repetidos. ID repetido: " + str(identif)
		else:
		    self.tablaSim[identif] = tipo

            self.analizaDeclV()
        elif self.componente.cat == "PR" and self.componente.valor =="INICIO" :
            pass
        else:
            print "Error: SE ESPERABA PR VAR O INICIO en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PR" and self.componente.valor == "INICIO"):
                self.avanza()
            return
    
    def analizaDeclV(self):
        if self.componente.cat == "Identif":
            listaIDs = self.analizaListaId()
            self.comprueba("DosPtos")
            tipo = self.analizaTipo()
            self.comprueba("PtoComa")

	    # RESTRICCION SEMANTICA: No puede haber identificadores repetidos
	    for identif in listaIDs:
		if (identif in self.tablaSim):
		    print "Error: no puede haber identificadores repetidos. ID repetido: " + str(identif)
		else:
		    self.tablaSim[identif] = tipo

            self.analizaDeclV()
        elif self.componente.cat == "PR" and self.componente.valor == "INICIO":
            pass
        else:
            print "Error: SE ESPERABA IDENTIFICADOR O PR INICIO en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PR" and self.componente.valor == "INICIO"):
                self.avanza()
            return
    
    def analizaListaId(self):
        if self.componente.cat == "Identif":
	    identif = self.componente.valor
            self.avanza()
            restoIds = self.analizaRestoListaId()
	    restoIds.append(identif)
	    return (restoIds)
        else:
            print "Error: SE ESPERABA IDENTIFICADOR en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaRestoListaId(self):
        if self.componente.cat == "Coma":
            self.avanza()
            restoIDs = self.analizaListaId()
	    return restoIDs
        elif self.componente.cat == "DosPtos":
            return []
        else:
            print "Error: SE ESPERABA COMA O DOS PUNTOS en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaTipo(self):
        if self.componente.cat =="PR"and self.componente.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            tipo = self.analizaTipoStd()
	    return tipo
        elif self.componente.cat == "PR" and self.componente.valor == "VECTOR":
            self.avanza()
            self.comprueba("CorAp")
            self.comprueba("Numero")
            self.comprueba("CorCi")
            self.analizaTipoStd()
	    return "VECTOR"
        else:
            print "Error: SE ESPERABA TIPO O VECTOR en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaTipoStd(self):
        if self.componente.cat =="PR"and self.componente.valor in ["ENTERO", "REAL", "BOOLEANO"]:
	    tipo = self.componente.valor
            self.avanza()
	    return tipo
        else:
            print "Error: TIPO INCORRECTO"
            while not (self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaInstrucciones(self):
        if self.componente.cat == "PR" and self.componente.valor == "INICIO":
            self.avanza()
            self.analizaListaInst()
            if self.componente.cat == "PR" and self.componente.valor == "FIN":
                self.avanza()
            else:
                print "Error: SE ESPERABA FIN en linea " + str(self.lexico.nlinea)
                while not (self.componente.cat == "Punto"):
                    self.avanza()
                return
        else:
            print "Error: SE ESPERABA INICIO en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "Punto"):
                self.avanza()
            return
    
    def analizaListaInst(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["INICIO", "SI", "ESCRIBE", "LEE", "MIENTRAS"]) or self.componente.cat == "Identif":
            self.analizaInstruccion()
            self.comprueba("PtoComa")
            self.analizaListaInst()
        elif self.componente.cat == "PR" and self.componente.valor == "FIN":
            pass
        else:
            print "Error: SE ESPERABA PR, Identificador o FIN en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PR" and self.componente.valor == "FIN"):
                self.avanza()
            return

    def analizaInstruccion(self):
        if self.componente.cat == "PR" and self.componente.valor == "INICIO":
            self.avanza()
            self.analizaListaInst()
            if self.componente.cat == "PR" and self.componente.valor == "FIN":
                self.avanza()
            else:
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
        elif self.componente.cat == "Identif":
            self.analizaInstSimple()
        elif self.componente.cat =="PR"and self.componente.valor in ["LEE", "ESCRIBE"]:
            self.analizaInstES()
        elif self.componente.cat == "PR" and self.componente.valor == "SI":
            self.avanza()
            self.analizaExpresion()
            if self.componente.cat == "PR" and self.componente.valor == "ENTONCES":
                self.avanza()
            else:
                print "Error: SE ESPERABA ENTONCES en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            self.analizaInstruccion()
            if self.componente.cat == "PR" and self.componente.valor == "SINO":
                self.avanza()
            else:
                print "Error: SE ESPERABA SINO en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            self.analizaInstruccion()
        elif self.componente.cat == "PR" and self.componente.valor == "MIENTRAS":
            self.avanza()
            self.analizaExpresion()
            if self.componente.cat == "PR" and self.componente.valor == "HACER":
                self.avanza()
            else:
                print "Error: SE ESPERABA HACER en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            self.analizaInstruccion()
        else: 
            print "Error: Instruccion invalida"
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaInstSimple(self):
        if self.componente.cat == "Identif":
            self.avanza()
            self.analizaRestoInstSimple()
        else: 
            print "Error: SE ESPERABA IDENTIFICADOR en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return
    
    def analizaRestoInstSimple(self):
        if self.componente.cat == "OpAsigna":
            self.avanza()
            self.analizaExpresion()
        elif self.componente.cat == "CorAp":
            self.avanza()
            self.analizaExprSimple()
            self.comprueba("CorCi")
            self.comprueba("OpAsigna")
            self.analizaExpresion()
        elif (self.componente.cat =="PR"and self.componente.valor in ["SINO"]) or self.componente.cat == "PtoComa":
            pass
        else:
            print "Error: SE ESPERABA OPASIGNA O CORAP en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return
    
    def analizaVariable(self):
        if self.componente.cat == "Identif":
            self.avanza()
            self.analizaRestoVar()
        else:
            print "Error: SE ESPERABA IDENTIFICADOR en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["Y","O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "OpMult" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaRestoVar(self):
        if self.componente.cat == "CorAp":
            self.avanza()
            self.analizaExprSimple()
            self.comprueba("CorCi")
        elif (self.componente.cat =="PR"and self.componente.valor in ["Y", "O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpMult" or self.componente.cat == "OpAdd" or self.componente.cat == "OpRel" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa" or self.componente.cat == "CorCi":
            pass
        else: 
            print "Error: SE ESPERABA CORAP en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["Y","O", "ENTERO", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "OpMult" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaInstES(self):
        if self.componente.cat == "PR" and self.componente.valor == "LEE":
            self.avanza()
            self.comprueba("ParentAp")
            self.comprueba("Identif")
            self.comprueba("ParentCi")
        elif self.componente.cat == "PR" and self.componente.valor == "ESCRIBE":
            self.avanza()
            self.comprueba("ParentAp")
            self.analizaExprSimple()
            self.comprueba("ParentCi")
        else: 
            print "Error: SE ESPERABA LEE O ESCRIBE en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaExpresion(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "Identif" or self.componente.cat == "Numero" or self.componente.cat == "ParentAp" or self.componente.cat == "OpAdd":
            self.analizaExprSimple()
            self.analizaExpresionPrima()
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES","HACER", "SINO"]) or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaExpresionPrima(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa" :
            pass
        elif self.componente.cat == "OpRel":
            self.avanza()
            self.analizaExprSimple()
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES","HACER", "SINO"]) or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaExprSimple(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "ParentAp" or self.componente.cat == "Identif" or self.componente.cat == "Numero":
            self.analizaTermino()
            self.analizaRestoExprSimple()
        elif self.componente.cat == "OpAdd":
            self.analizaSigno()
            self.analizaTermino()
            self.analizaRestoExprSimple()
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea) 
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaRestoExprSimple(self):
        if self.componente.cat == "OpAdd":
            self.avanza()
            self.analizaTermino()
            self.analizaRestoExprSimple()
        elif self.componente.cat == "PR" and self.componente.valor == "O":
            self.avanza()
            self.analizaTermino()
            self.analizaRestoExprSimple()
        elif (self.componente.cat =="PR"and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "ParentCi" or self.componente.cat == "CorCi" or self.componente.cat == "OpRel" or self.componente.cat == "PtoComa":
            pass
        else: 
            print "Error: SE ESPERABA Comienzo de Resto Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
        
    def analizaTermino(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "ParentAp" or self.componente.cat == "Identif" or self.componente.cat == "Numero":
            self.analizaFactor()
            self.analizaRestoTerm()
        else: 
            print "Error: SE ESPERABA Termino en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaRestoTerm(self):
        if self.componente.cat == "OpMult":
            self.avanza()
            self.analizaFactor()
            self.analizaRestoTerm()
        elif self.componente.cat == "PR" and self.componente.valor == "Y":
            self.avanza()
            self.analizaFactor()
            self.analizaRestoTerm()
        elif (self.componente.cat =="PR"and self.componente.valor in ["ENTONCES", "HACER", "SINO", "O"]) or self.componente.cat == "ParentCi" or self.componente.cat == "CorCi" or self.componente.cat == "OpRel" or self.componente.cat == "PtoComa" or self.componente.cat == "OpAdd":
            pass
        else: 
            print "Error: SE ESPERABA Resto de Termino en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
        
    def analizaFactor(self):
        if self.componente.cat == "Identif":
            self.analizaVariable()
        elif self.componente.cat == "Numero":
            self.avanza()
        elif self.componente.cat == "ParentAp":
            self.avanza()
            self.analizaExpresion()
            self.comprueba("ParentCi")
        elif self.componente.cat == "PR" and self.componente.valor == "NO":
            self.avanza()
            self.analizaFactor()
        elif self.componente.cat == "PR" and self.componente.valor == "CIERTO":
            self.avanza()
        elif self.componente.cat == "PR" and self.componente.valor == "FALSO":
            self.avanza()
        
        else: 
            print "Error: SE ESPERABA Factor en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["Y","O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "OpMult" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return

    def analizaSigno(self):
        if self.componente.cat == "OpAdd":
            self.avanza()
        
        else: 
            print "Error: SE ESPERABA Operador Suma o Resta en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["NO","CIERTO", "FALSO"]) or self.componente.cat == "Identif" or self.componente.cat == "Numero" or self.componente.cat == "ParentAp"):
                self.avanza()
            return

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador sintactico
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
    analex=analex.Analex(fl)
    anasint = Anasint(analex)
    


