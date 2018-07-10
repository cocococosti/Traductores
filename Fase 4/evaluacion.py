import sys

class evaluacion():
	def __init__(self, tablaSim):
		self.tabla = tablaSim
		
		
	def evalArbol(self,ast):
		if (ast):
				if (len(ast.hijos) > 0): 

					for nodo in ast.hijos:
						if (nodo.tipo == 'ASIGNACION'):
							var = nodo.valor
							value = self.evalExp(nodo.hijos[0])
							self.setValor(var, value)

						elif (nodo.tipo == 'VARIABLE'):
							for i in nodo.hijos:
								if (i.tipo == 'EXPRESION'):
									var = nodo.valor

									value = self.evalExp(i)
									self.setValor(var, value)

						elif (nodo.tipo == 'DECLARACION'):
							for i in nodo.hijos:

								self.evalArbol(i)
							
						else:
							self.evalArbol(nodo)

	def evalExp(self, exp):
		if (exp.tipo == 'TERMINO'):
			if (len(exp.hijos)>0):
				t = self.evalExp(exp.hijos[0])
				return t
			else:

				if (exp.type == 'var'):
					t = self.getValor(exp.lexeme)
					return t
				else:
					if (exp.lexeme == 'true'):
						return True
					elif (exp.lexeme == 'false'):
						return False
					else:
						return exp.lexeme

		elif (exp.tipo == 'BOOLEANA'):
			operacion = exp.valor
			op1 = self.evalExp(exp.hijos[0])
			op2 = self.evalExp(exp.hijos[1])
			if (operacion == '\/'):
				res = op1 or op2
			elif (operacion == '/\\'):
				res = op1 and op2

			return res

		elif (exp.tipo == 'BOOLEANA UNARIA'):
			op = self.evalExp(exp.hijos[0])
			return not op

		elif (exp.tipo == 'RELACIONAL'):
			operacion = exp.valor
			op1 = self.evalExp(exp.hijos[0])
			op2 = self.evalExp(exp.hijos[1])

			if (operacion == '<'):
				res = op1 < op2
			elif (operacion == '>'):
				res = op1 > op2
			elif (operacion == '<='):
				res = op1 <= op2
			elif (operacion == '>='):
				res = op1 >= op2
			elif (operacion == '='):
				res = op1 == op2
			elif (operacion == '/='):
				res = op1 != op2

			return res

		elif (exp.tipo == 'OPERACION CARACTER'):

			operacion = exp.valor
			op = self.evalExp(exp.hijos[0])
			op = op.strip('\'')


			if (operacion == '#'):
				return ord(op)
			elif (operacion == '++'):
				if(ord(op)==127):
					return chr(0)
				else:	
					return chr(ord(op)+1)
			elif (operacion == '--'):
				if (ord(op)==0):
					return chr(127)
				else:
					return chr(ord(op)-1)

		elif(exp.tipo == 'EXPRESION'):
			t = self.evalExp(exp.hijos[0])

		return t

	def setValor(self, var, val):
		if (len(self.tabla) > 0):

			for i in range(len(self.tabla)):
				if var in self.tabla[i]:
					self.tabla[i][var].res = val

	def getValor(self, var):
		val = None
		if (len(self.tabla) > 0):

			for i in range(len(self.tabla)):
				if var in self.tabla[i]:
					val = self.tabla[i][var].res

		if (val):
			return val
		else:
			print("Error. Variable " + var + " no inicializada.")
			sys.exit(0)



