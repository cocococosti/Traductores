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
							if (isinstance(var, str)):
								self.setValor(var, value)
							else:
								indice = self.evalExp(var.hijos[0])
								self.setValor(var.valor, value, indice)

								

						elif (nodo.tipo == 'VARIABLE'):
							for i in nodo.hijos:
								if (i.tipo == 'EXPRESION'):
									var = nodo.valor

									value = self.evalExp(i)
									self.setValor(var, value)

						elif (nodo.tipo == 'DECLARACION'):
							for i in nodo.hijos:

								self.evalArbol(i)

						elif (nodo.tipo == 'SALIDA'):
							val = self.evalExp(nodo.hijos[0])
							print(val)

						elif (nodo.tipo == 'ENTRADA'):
							val = input()
							var = nodo.valor

							# chequear que la entrada del user sea del tipo correcto (int, bool, char)
							# arreglar contexto, debe chequear que la var a leer este declarada!
							
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

		elif (exp.tipo == 'BIN_ARITMETICA'):
			operacion = exp.valor
			op1 = self.evalExp(exp.hijos[0])
			op2 = self.evalExp(exp.hijos[1])
			if (operacion == '+'):
				res = op1 + op2
			elif (operacion == '-'):
				res = op1 - op2
			elif (operacion == '*'):
				res = op1 * op2
			elif (operacion == '/'):
				if (op2 == 0):
					print("Error division por cero")
					sys.exit(0)
				else:
					res = op1 / op2
				
			elif (operacion == '%'):
				res = op1 % op2
			
			return int(res)
		
		elif (exp.tipo == 'OPERACION UNARIA'):
			op = self.evalExp(exp.hijos[0])
			return -op

		elif(exp.tipo == 'EXPRESION'):
			t = self.evalExp(exp.hijos[0])

		elif(exp.tipo == 'VAR_ARREGLO'):
			indice = self.evalExp(exp.hijos[0])
			v = self.getValor(exp.valor, indice)
			return v

		elif (exp.tipo == 'OPERACION ARREGLO'):
			if (len(exp.hijos)==2):
				op1 = self.evalExp(exp.hijos[0])
				op2 = self.evalExp(exp.hijos[1])
				res = op1.extend(op2)
				return res
			else:
				op = self.evalExp(exp.hijos[0])


		return t

	def setValor(self, var, val, index=None):
		if (len(self.tabla) > 0):

			for i in range(len(self.tabla)):
				if var in self.tabla[i]:
					if (index):
						if (index > self.evalExp(self.tabla[i][var].size)):
							print("Error. Indice excede tamaño del arreglo.")
							sys.exit(0)
						elif (index < 0):
							print("Error. Indice no puede ser negativo.")
							sys.exit(0)
						else:
							if (len(self.tabla[i][var].res)==0):
								for n in range(self.evalExp(self.tabla[i][var].size)):
									self.tabla[i][var].res.append(None)

							if (isinstance(val, list)):
								if (not self.tabla[i][var].arreglo):
									print("Error. No se puede asignar arreglo a entero.")
									sys.exit(0)
							self.tabla[i][var].res[index] = val
					else:
						if (isinstance(val, list)):
							if (not self.tabla[i][var].arreglo):
								print("Error. No se puede asignar arreglo a entero.")
								sys.exit(0)
						self.tabla[i][var].res = val

	def getValor(self, var, index=None):
		val = None
		if (len(self.tabla) > 0):

			for i in range(len(self.tabla)):
				if var in self.tabla[i]:
					if (index):
						if (self.tabla[i][var].arreglo):
							if (index < 0):
								print("Error. Indice no puede ser negativo.")
								sys.exit(0)

							if (len(self.tabla[i][var].res)!=0):

								val = self.tabla[i][var].res[index]
						else:
							print("Error. Variable no es un arreglo.")
							sys.exit(0)
					else:	
						val = self.tabla[i][var].res


		if (val != None):
			return val
		else:
			print("Error. Variable " + var + " no inicializada.")
			sys.exit(0)




