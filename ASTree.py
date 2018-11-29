#!/usr/bin/env python

class AST:
	def __str__(self):
		return self.arbol(self)

class NodoAsignacion(AST):
	def __init__(self, izda, exp, linea):
		self.izda = izda
		self.exp = exp
		self.linea = linea

	def compsem(self):
		tipoiz = self.izda.tipo
		tipodc = self.exp.tipo

		# Comprobaciones de compatibilidad de tipos
		if (tipoiz == "Booleano"):
			if (tipodc != "Booleano"):
				print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"

		elif (tipoiz == "Real"):
			if (tipodc == "Booleano"):
				print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"

		elif (tipoiz == "Entero"):
			if (tipodc == "Real"):
				print "Error: no se puede truncar un real a un entero (error semantico en linea " + str(self.linea) + ")"

			elif (tipodc == "Booleano"):
				print "Error: el tipo entero es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"

	def arbol(self):
		pass

class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea

	def compsem(self):
		# Nada que ver aqui, sigan circulando...
		pass

	def arbol(self):
		pass

class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea

	def compsem(self):
		# No hay nada raro por aqui...
		pass

	def arbol(self):
		pass

class NodoLee(AST):
	def __init__(self,var,linea):
		self.var = var
		self.linea = linea

	def compsem(self):
		# La variable a leer solo puede ser entera o real
		if (self.var.tipo == "Booleano"):
			print "Error: no se puede leer por teclado una variable booleana (error semantico en linea " + str(self.linea) + ")"

	def arbol(self):
		pass

class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea

	def compsem(self):
		# Nothing to see here, gentlemen...
		pass

	def arbol(self):
		pass

class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea

	def compsem(self):
		# Nada por aqui, nada por alla...
		pass

	def arbol(self):
		pass

class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None

	
	def compsem(self):
		if self.izq.tipo == "Entero":
			if self.dcha.tipo == "Booleano":
				print "Error: el tipo entero es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			elif self.dcha.tipo == "Real":
				self.tipo == "Real"
			else:
				self.tipo == "Entero"

		if self.izq.tipo == "Real":
			if self.dcha.tipo == "Booleano":
				print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "Real"
		
		if self.izq.tipo == "Booleano":
			if self.dcha.tipo is not "Booleano":
				print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "Booleano"

	def arbol(self):
		#Wiiiiii
		pass

class NodoAritmetico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None

	
	def compsem(self):
		if self.izq.tipo == "Entero":
			if self.dcha.tipo == "Booleano":
				print "Error: el tipo entero es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			elif self.dcha.tipo == "Real":
				self.tipo == "Real"
			else:
				self.tipo == "Entero"

		if self.izq.tipo == "Real":
			if self.dcha.tipo == "Booleano":
				print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "Real"
		
		if self.izq.tipo == "Booleano":
			if self.dcha.tipo is not "Booleano":
				print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "Booleano"

	def arbol(self):
		#Super Wiiiiii
		pass


class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "Entero"
	
	def arbol(self):
		pass


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "Real"
	
	def arbol(self):
		pass

class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "Booleano"
	
	def arbol(self):
		pass
