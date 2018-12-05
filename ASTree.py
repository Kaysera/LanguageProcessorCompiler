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
		self.izda.compsem()
		self.exp.compsem()
		tipoiz = self.izda.tipo
		tipodc = self.exp.tipo

		# Comprobaciones de compatibilidad de tipos
		if (tipoiz == "BOOLEANO"):
			if (tipodc != "BOOLEANO"):
				print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"

		elif (tipoiz == "REAL"):
			if (tipodc == "BOOLEANO"):
				print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"

		elif (tipoiz == "ENTERO"):
			if (tipodc == "REAL"):
				print "Error: no se puede truncar un real a un ENTERO (error semantico en linea " + str(self.linea) + ")"

			elif (tipodc == "BOOLEANO"):
				print "Error: el tipo ENTERO es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"

	def arbol(self):
		return '( "Asignacion"\n  "linea: %d" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)

class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea

	def compsem(self):
		self.exp.compsem()
		self.si.compsem()
		self.sino.compsem()

	def arbol(self):
		return '( "Si" "linea: %d" %s\n %s\n %s\n )' % (self.linea, self.exp, self.si, self.sino)

class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea

	def compsem(self):
		self.exp.compsem()
		self.inst.compsem()

	def arbol(self):
		return '( "Mientras" "linea: %d" %s\n %s\n )' % (self.linea, self.exp, self.inst)

class NodoLee(AST):
	def __init__(self,var,linea):
		self.var = var
		self.linea = linea

	def compsem(self):
		# La variable a leer solo puede ser entera o real
		if (self.var.tipo == "BOOLEANO"):
			print "Error: no se puede leer por teclado una variable booleana (error semantico en linea " + str(self.linea) + ")"

	def arbol(self):
		return '( "Lee" "linea: %d" %s )' % (self.linea, self.var)

class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea

	def compsem(self):
		self.exp.compsem()

	def arbol(self):
		return '( "Escribe" "linea: %d" %s )' % (self.linea, self.exp)

class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea

	def compsem(self):
		for inst in self.lsen:
			inst.compsem()

	def arbol(self):
		r= ""
    		for sent in self.lsen:
      			r+= sent.arbol()+"\n"
    		return '( "Compuesta"\n %s)' % r

class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None

	
	def compsem(self):
		self.izq.compsem()
		self.dcha.compsem()

		if self.izq.tipo == "ENTERO":
			if self.dcha.tipo == "BOOLEANO":
				print "Error: el tipo ENTERO es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			elif self.dcha.tipo == "REAL":
				self.tipo == "REAL"
			else:
				self.tipo == "ENTERO"

		if self.izq.tipo == "REAL":
			if self.dcha.tipo == "BOOLEANO":
				print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "REAL"
		
		if self.izq.tipo == "BOOLEANO":
			if self.dcha.tipo is not "BOOLEANO":
				print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"
			else:
				self.tipo == "BOOLEANO"

	def arbol(self):
		return '( "Comparacion" "op: %s" "tipo: %s" "linea: %d" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoAritmetico(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None

	
	def compsem(self):
		self.izq.compsem()
		self.dcha.compsem()

		if self.izq is not None:
			if self.izq.tipo == "ENTERO":
				if self.dcha.tipo == "BOOLEANO":
					print "Error: el tipo ENTERO es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
				elif self.dcha.tipo == "REAL":
					self.tipo == "REAL"
				else:
					self.tipo == "ENTERO"

			if self.izq.tipo == "REAL":
				if self.dcha.tipo == "BOOLEANO":
					print "Error: el tipo real es incompatible con el tipo booleano (error semantico en linea " + str(self.linea) + ")"
				else:
					self.tipo == "REAL"
		
			if self.izq.tipo == "BOOLEANO":
				if self.dcha.tipo is not "BOOLEANO":
					print "Error: El tipo booleano es incompatible con tipos no booleanos (error semantico en linea " + str(self.linea) + ")"
				else:
					self.tipo == "BOOLEANO"

		else:
			self.tipo = self.dcha.tipo

	def arbol(self):
		return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %d" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "ENTERO"
	
	def arbol(self):
		return '( "Entero" "valor: %d" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "REAL"
	
	def arbol(self):
		return '( "Real" "valor: %d" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)

class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
	
	def compsem(self):
		self.tipo = "BOOLEANO"
	
	def arbol(self):
		return '( "BOOLEANO" "valor: %d" "tipo: %s" "linea: %d" )' % (self.valor, self.tipo, self.linea)

class NodoAccesoVariable(AST):
	def __init__(self, var, linea, tipo):
		self.var = var
		self.linea = linea
		self.tipo = tipo

	def compsem(self):
		pass

	def arbol(self):
		return '( "AccesoVariable" "v: %s" "linea: %d" )' % (self.var, self.linea)

class NodoAccesoVector(AST):
	def __init__(self, vect, exp, linea):
		self.vect = vect
		self.exp = exp
		self.linea = linea

	def compsem(self):
		self.exp.compsem()

		if self.exp.tipo is not "ENTERO":
			print "Error: No se puede indexar un vector con un tipo no ENTERO (error semantico en linea " + str(self.linea) + ")"

		if self.vect.tipo is not "VECTOR":
			print "Error: no se puede indexar un tipo no vectorial (error semantico en linea " + str(self.linea) + ")"

		self.tipo = self.vect.tipo

	def arbol(self):
		return '( "AccesoVector" "tipo: %s" "linea: %d" %s\n %s\n)' % (self.tipo, self.linea, self.vect, self.exp)
