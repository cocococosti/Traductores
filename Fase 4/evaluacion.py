import sys
from collections import deque
from contexto import *

class evaluacion():
	# Usamos tabla de simbolos para obtener las variables del programa
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
								else:
									self.evalArbol(nodo)

						elif (nodo.tipo == 'DECLARACION'):
							
							self.evalArbol(nodo)

						elif (nodo.tipo == 'SALIDA'):
							val = self.evalExp(nodo.hijos[0])

							print(val)

						elif (nodo.tipo == 'ENTRADA'):
							val = input()
							var = nodo.valor
							if (val.isdigit()):
								val = int(val)
							if (val == 'false'):
								val = False
							elif (val == 'true'):
								val = True
							for i in self.tabla:
								if var in i:
									t = i[var].tipo
									if (isinstance(val,str) and t!='char'):
										print("Error. Tipo incorrecto")
										sys.exit(0)
									elif(isinstance(val,bool) and t!='bool'):
										print("Error. Tipo incorrecto")
										sys.exit(0)
									elif(isinstance(val, int) and t!= 'int'):
										print("Error. Tipo incorrecto")
										sys.exit(0)
							self.setValor(var, val)

							# chequear que la entrada del user sea del tipo correcto (int, bool, char)
							# arreglar contexto, debe chequear que la var a leer este declarada!
						elif (nodo.tipo == 'CONDICIONAL'):
							guardia = self.evalExp(nodo.hijos[0])
							cuerpo = nodo.hijos[1]
							if (guardia):
								self.evalArbol(cuerpo)
							else:

								if (len(nodo.hijos)==3):
									other = nodo.hijos[2]
									self.evalArbol(other)
						elif (nodo.tipo == 'ITERACION DETERMINADA'):
							val = self.getValor(nodo.valor[0],None,True)
							contador = simbolo(self.getValor(nodo.valor[0],None,True),'int')
							self.tabla.insert(0,{})
							self.tabla[0][nodo.valor[0]]=contador
							liminf = self.evalExp(nodo.valor[1])
							self.setValor(nodo.valor[0], liminf)
							limsup = self.evalExp(nodo.valor[2])
							step = nodo.valor[3]

							if (isinstance(step,str)):
								step = int(step)
							else:
								step = self.evalExp(step)
							if (step == 0):
								print("Error. El paso en la iteracion determinada no puede ser 0.")
								sys.exit(0)
							# step distinta de 0 !
							for i in range(liminf, limsup, step):
								self.setValor(nodo.valor[0], i)
								self.evalArbol(nodo.hijos[0])
							self.setValor(nodo.valor[0], val)
							self.tabla.pop(0)
						
									
									
						elif (nodo.tipo == 'ITERACION INDETERMINADA'):
							exp = self.evalExp(nodo.valor)
							while (exp):
								self.evalArbol(nodo.hijos[0])
								comprobarexp = self.evalExp(nodo.valor)
								if (comprobarexp):
									continue
								else:
									break


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

				op1 = self.getValor(exp.hijos[0])
				op2 = self.getValor(exp.hijos[1])
				res = op1+op2
				return res
			else:
				op = self.getValor(exp.hijos[0])
				temp = []
				temp.append(op[len(op)-1])
				for i in range(len(op)-1):
					temp.append(op[i])
				return temp

		return t

	def isArray(self, var):
		if (isinstance(var, str) and len(var)==1):
			if (len(self.tabla) > 0):

				for i in range(len(self.tabla)):
					if var in self.tabla[i]:
						if (self.tabla[i][var].arreglo):
							return True
		return False

	def setValor(self, var, val, index=None):
		if (len(self.tabla) > 0):

			for i in range(len(self.tabla)):
				if var in self.tabla[i]:

					# Chequeamos si se estan asignando arreglos
					if (self.tabla[i][var].arreglo and not self.isArray(val) and index==None):
						print("Error. No se puede asignar un arreglo.")
						sys.exit(0)
					elif (not self.tabla[i][var].arreglo and self.isArray(val)):
						print("Error. No se puede asignar un arreglo.")
						sys.exit(0)

					if (index!=None):
						if (index >= self.evalExp(self.tabla[i][var].size)):
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
								print("Error. No se puede asignar arreglo a variable que no es arreglo.")
								sys.exit(0)
							if (len(val) > self.evalExp(self.tabla[i][var].size)):
								print("Error. Arreglo excede el tamaño de la variable.")
								sys.exit(0)


						self.tabla[i][var].res = val

	def getValor(self, var, index=None, itera=None):
		# Valor a buscar
		val = None
		# Recorremos tabla
		if (len(self.tabla) > 0):
			for i in range(len(self.tabla)):
				# Si encontramos variable en la tabla
				if var in self.tabla[i]:
					# Si estamos buscando indice
					if (index!=None):
						# Si la variable es un arreglo
						if (self.tabla[i][var].arreglo):
							# Indice negativo reporta error
							if (index < 0):
								print("Error. Indice no puede ser negativo.")
								sys.exit(0)
							# Indice mayor que el tamaño del arreglo reporta error
							elif (index >= self.evalExp(self.tabla[i][var].size)):
								print("Error. Indice excede tamaño del arreglo.")
								sys.exit(0)
							# Si la variable esta inicializada
							if (self.tabla[i][var].res!=None):
								if (len(self.tabla[i][var].res)!=0):

									val = self.tabla[i][var].res[index]
						else:
							print("Error. Variable no es un arreglo.")
							sys.exit(0)
					else:	
						val = self.tabla[i][var].res


		if (val != None):
			return val
		elif (val==None and index!=None):
			return val
		elif(itera!=None):
			return val
		else:
			if (index != None):

				print("Error. Variable " + var + "[" + str(index) +"] no inicializada.")
				sys.exit(0)
			else:
				print("Error. Variable " + var + " no inicializada.")
				sys.exit(0)




