#!/usr/bin/env python

import componentes
import flujo
import string
import sys
import analex
import ASTree as AST

from sys import argv
from sets import ImmutableSet

class Anasint:
    def __init__(self, lexico):
        self.ast = []
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
            while not (self.componente.cat == "EOF"):
                self.avanza()
            return
    
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
	    if self.componente.cat == "PR" and self.componente.valor == "DE":
                self.avanza()
            else:
                print "Error: SE ESPERABA DE en linea " + str(self.lexico.nlinea)
                while not (self.componente.cat == "PtoComa"):
			self.avanza()
		return
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
            self.ast = self.analizaListaInst()
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
            inst = self.analizaInstruccion()
            self.comprueba("PtoComa")
            linst = self.analizaListaInst()
            return [inst] + linst
        elif self.componente.cat == "PR" and self.componente.valor == "FIN":
	        return []
        else:
            print "Error: SE ESPERABA PR, Identificador o FIN en linea " + str(self.lexico.nlinea)
            while not (self.componente.cat == "PR" and self.componente.valor == "FIN"):
                self.avanza()
            return

    def analizaInstruccion(self):
        if self.componente.cat == "PR" and self.componente.valor == "INICIO":
            self.avanza()
            linst = self.analizaListaInst()
            if self.componente.cat == "PR" and self.componente.valor == "FIN":
                self.avanza()
                return AST.NodoCompuesta(linst, self.lexico.nlinea)
            else:
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
        elif self.componente.cat == "Identif":
            return self.analizaInstSimple()
        elif self.componente.cat =="PR"and self.componente.valor in ["LEE", "ESCRIBE"]:
            return self.analizaInstES()
        elif self.componente.cat == "PR" and self.componente.valor == "SI":
            self.avanza()
            expr = self.analizaExpresion()
            if self.componente.cat == "PR" and self.componente.valor == "ENTONCES":
                self.avanza()
            else:
                print "Error: SE ESPERABA ENTONCES en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            instSi = self.analizaInstruccion()
            if self.componente.cat == "PR" and self.componente.valor == "SINO":
                self.avanza()
            else:
                print "Error: SE ESPERABA SINO en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            instSino = self.analizaInstruccion()
            return AST.NodoSi(expr, instSi, instSino, self.lexico.nlinea)
        elif self.componente.cat == "PR" and self.componente.valor == "MIENTRAS":
            self.avanza()
            expr = self.analizaExpresion()
            if self.componente.cat == "PR" and self.componente.valor == "HACER":
                self.avanza()
            else:
                print "Error: SE ESPERABA HACER en linea " + str(self.lexico.nlinea)
                while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
                return
            inst = self.analizaInstruccion()
            return AST.NodoMientras(expr, inst, self.lexico.nlinea)
        else: 
            print "Error: Instruccion invalida"
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaInstSimple(self):
        if self.componente.cat == "Identif":
	    # RESTRICCION SEMANTICA: definir variables antes de usarlas
            if (self.componente.valor not in self.tablaSim):
                print "Error: variable no definida: '" + self.componente.valor + "' en linea " + str(self.componente.linea)
            accVar = AST.NodoAccesoVariable(self.componente.valor, self.lexico.nlinea, self.tablaSim[self.componente.valor])
            self.avanza()
            expr = self.analizaRestoInstSimple()
            nodoAsignacion = AST.NodoAsignacion(accVar, expr, self.lexico.nlinea)
            return nodoAsignacion
        else: 
            print "Error: SE ESPERABA IDENTIFICADOR en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return
    
    def analizaRestoInstSimple(self):
        if self.componente.cat == "OpAsigna":
            self.avanza()
            return self.analizaExpresion()
        elif self.componente.cat == "CorAp":
            self.avanza()
            self.analizaExprSimple()
            self.comprueba("CorCi")
            self.comprueba("OpAsigna")
            return self.analizaExpresion()
        elif (self.componente.cat =="PR"and self.componente.valor in ["SINO"]) or self.componente.cat == "PtoComa":
            pass
        else:
            print "Error: SE ESPERABA OPASIGNA O CORAP en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return
    
    def analizaVariable(self):
        if self.componente.cat == "Identif":
	    # RESTRICCION SEMANTICA: definir variables antes de usarlas
	    if (self.componente.valor not in self.tablaSim):
	        print "Error: variable no definida: '" + self.componente.valor + "' en linea " + str(self.componente.linea)

	    var = self.componente.valor
	    tipo = self.tablaSim[var]
            self.avanza()
            dcha = self.analizaRestoVar()
	
	    if (dcha is None):
		return AST.NodoAccesoVariable(var, self.lexico.nlinea, tipo)

	    else:
		return AST.NodoAccesoVector(var, dcha, self.lexico.nlinea)
        else:
            print "Error: SE ESPERABA IDENTIFICADOR en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["Y","O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "OpMult" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaRestoVar(self):
        if self.componente.cat == "CorAp":
            self.avanza()
            expr = self.analizaExprSimple()
            self.comprueba("CorCi")
	    return expr
        elif (self.componente.cat =="PR"and self.componente.valor in ["Y", "O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpMult" or self.componente.cat == "OpAdd" or self.componente.cat == "OpRel" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa" or self.componente.cat == "CorCi":
            return None
        else: 
            print "Error: SE ESPERABA CORAP en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["Y","O", "ENTERO", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "OpMult" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaInstES(self):
        if self.componente.cat == "PR" and self.componente.valor == "LEE":
            self.avanza()
            self.comprueba("ParentAp")
	        # RESTRICCION SEMANTICA: el argumento de LEE solo puede ser entero o real
            if (self.tablaSim[self.componente.valor] not in ["ENTERO", "REAL"]):
                print "Error: el tipo a leer solo puede ser entero o real (instruccion LEE en linea " + str(self.componente.linea) + ")"

            nodoLee = AST.NodoLee(self.componente.valor, self.lexico.nlinea)
            self.comprueba("Identif")
            self.comprueba("ParentCi")
            return nodoLee
        elif self.componente.cat == "PR" and self.componente.valor == "ESCRIBE":
            self.avanza()
            self.comprueba("ParentAp")
            expr = self.analizaExprSimple()
            self.comprueba("ParentCi")
            nodoEscribe = AST.NodoEscribe(expr, self.lexico.nlinea)
            return nodoEscribe
        else: 
            print "Error: SE ESPERABA LEE O ESCRIBE en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor == "SINO") or self.componente.cat == "PtoComa"):
                    self.avanza()
            return

    def analizaExpresion(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "Identif" or self.componente.cat == "Numero" or self.componente.cat == "ParentAp" or self.componente.cat == "OpAdd":
            izd = self.analizaExprSimple()
            dcha = self.analizaExpresionPrima()
            if dcha is None:
                return izd
            else:
                nodoComp = AST.NodoComparacion(izd, dcha[0], self.lexico.nlinea, dcha[1])
                return nodoComp
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES","HACER", "SINO"]) or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaExpresionPrima(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa" :
            return None
        elif self.componente.cat == "OpRel":
            op = self.componente.valor
            self.avanza()
            arb = self.analizaExprSimple()
            return [arb, op]
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES","HACER", "SINO"]) or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaExprSimple(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "ParentAp" or self.componente.cat == "Identif" or self.componente.cat == "Numero":
            term = self.analizaTermino()
            return self.analizaRestoExprSimple(term)
        elif self.componente.cat == "OpAdd":
            signo = self.componente.valor
            self.analizaSigno()
            term = self.analizaTermino()
            dcha = self.analizaRestoExprSimple(term)
            return AST.NodoAritmetico(None, dcha, self.lexico.nlinea, signo)
        else: 
            print "Error: SE ESPERABA Comienzo de Expresion Simple en linea " + str(self.lexico.nlinea) 
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaRestoExprSimple(self, hered):
        if self.componente.cat == "OpAdd":
            op = self.componente.valor
            self.avanza()
            term = self.analizaTermino()
            nodoSuma = AST.NodoAritmetico(hered, term, self.lexico.nlinea, op)
            return self.analizaRestoExprSimple(nodoSuma)
        elif self.componente.cat == "PR" and self.componente.valor == "O":
            self.avanza()
            term = self.analizaTermino()
            nodoCuasiSuma = AST.NodoAritmetico(hered, term, self.lexico.nlinea, "O")
            return self.analizaRestoExprSimple(nodoCuasiSuma)
        elif (self.componente.cat =="PR"and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "ParentCi" or self.componente.cat == "CorCi" or self.componente.cat == "OpRel" or self.componente.cat == "PtoComa":
            return hered
        else: 
            print "Error: SE ESPERABA Comienzo de Resto Expresion Simple en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
        
    def analizaTermino(self):
        if (self.componente.cat =="PR"and self.componente.valor in ["NO", "CIERTO", "FALSO"]) or self.componente.cat == "ParentAp" or self.componente.cat == "Identif" or self.componente.cat == "Numero":
            izq = self.analizaFactor()
            return self.analizaRestoTerm(izq)
        else: 
            print "Error: SE ESPERABA Termino en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
    
    def analizaRestoTerm(self, hered):
        if self.componente.cat == "OpMult":
            op = self.componente.valor
            self.avanza()
            fact = self.analizaFactor()
            nodoMult = AST.NodoAritmetico(hered, fact, self.lexico.nlinea, op)
            return self.analizaRestoTerm(nodoMult)
        elif self.componente.cat == "PR" and self.componente.valor == "Y":
            self.avanza()
            fact = self.analizaFactor()
            nodoCuasiMult = AST.NodoAritmetico(hered, fact, self.lexico.nlinea, "Y")
            return self.analizaRestoTerm(nodoCuasiMult)
        elif (self.componente.cat == "PR" and self.componente.valor in ["ENTONCES", "HACER", "SINO", "O"]) or self.componente.cat == "ParentCi" or self.componente.cat == "CorCi" or self.componente.cat == "OpRel" or self.componente.cat == "PtoComa" or self.componente.cat == "OpAdd":
            return hered
        else: 
            print "Error: SE ESPERABA Resto de Termino en linea " + str(self.lexico.nlinea)
            while not ((self.componente.cat == "PR" and self.componente.valor in ["O", "ENTONCES", "HACER", "SINO"]) or self.componente.cat == "OpRel" or self.componente.cat == "OpAdd" or self.componente.cat == "CorCi" or self.componente.cat == "ParentCi" or self.componente.cat == "PtoComa"):
                self.avanza()
            return
        
    def analizaFactor(self):
        if self.componente.cat == "Identif":
            return self.analizaVariable()
        elif self.componente.cat == "Numero":
            nodo = None
            if self.componente.tipo is "ENTERO":
                nodo = AST.NodoEntero(self.componente.valor, self.lexico.nlinea)
            else:
                nodo = AST.NodoReal(self.componente.valor, self.lexico.nlinea)
            self.avanza()
            return nodo
        elif self.componente.cat == "ParentAp":
            self.avanza()
            nodo = self.analizaExpresion()
            self.comprueba("ParentCi")
            return nodo
        elif self.componente.cat == "PR" and self.componente.valor == "NO":
            self.avanza()
            fact = self.analizaFactor()
            return AST.NodoAritmetico(None, fact, self.lexico.nlinea, "NO")
        elif self.componente.cat == "PR" and self.componente.valor == "CIERTO":
            self.avanza()
            return AST.NodoBooleano("CIERTO", self.lexico.nlinea)
        elif self.componente.cat == "PR" and self.componente.valor == "FALSO":
            self.avanza()
            return AST.NodoBooleano("FALSO", self.lexico.nlinea)
        
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

    print (anasint.ast)

    for nodo in anasint.ast:
        if nodo is not None:
	        print nodo.arbol()
