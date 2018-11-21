#!/usr/bin/env python

class AST:
	def __str__(self):
		return self.arbol()

class NodoAsignacion(AST):
	def __init__(self, izda, exp, linea):
		self.izda = izda
		self.exp = exp
		self.linea = linea

	def compsem():
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

	def arbol():
		pass

class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea

	def compsem():
		# Nada que ver aqui, sigan circulando...
		pass

	def arbol():
		pass

class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea

	def compsem():
		# No hay nada raro por aqui...
		pass

	def arbol():
		pass

class NodoLee(AST):
	def __init__(self,var,linea):
		self.var = var
		self.linea = linea

	def compsem():
		# La variable a leer solo puede ser entera o real
		if (self.var.tipo == "Booleano"):
			print "Error: no se puede leer por teclado una variable booleana (error semantico en linea " + str(self.linea) + ")"

	def arbol():
		pass

class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea

	def compsem():
		# Nothing to see here, gentlemen...
		pass

	def arbol():
		pass

class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea

	def compsem():
		# Nada por aqui, nada por alla...
		pass

	def arbol():
		pass

