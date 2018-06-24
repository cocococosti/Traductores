import sys

class context:
	def __init__(self):
		self.scopes = []

	def contextCheck(self, ast):
		if (ast):
			if (len(ast.hijos) > 0):
				for hijo in ast.hijos:
					if (hijo.tipo == 'DECLARACION'):
						scope = {}
						self.scopes.insert(0, scope)

						tipo = hijo.valor
						for k in hijo.hijos:
							if (k.tipo == 'ARREGLO'):
								tipo = self.getTipoArreglo(k)
							
						self.nuevoScope(hijo, tipo)

						top = self.scopes[0]

					elif (hijo.tipo == 'ASIGNACION'):
						var = self.checkVar(hijo.valor)
							
					elif (hijo.tipo == 'ENTRADA' or hijo.tipo == 'SALIDA' or hijo.tipo == 'TERMINO'):
						pass
					else:
						self.contextCheck(hijo) 

	def checkExp(self, exp):
		# Chequea si las operaciones de la expr son correctas
		# y retorna el tipo resultante 
		# Usarla de forma recursiva con cada subexpresion
		# retorna error si se obtiene tipos distintos
		if (exp.tipo == 'RELACIONAL' or exp.tipo == 'BOOLEANA'):
			op1 = op.hijos[0]
			op2 = op.hijos[1]
			tipo1 = self.checkExp(op1)
			tipo2 = self.checkExp(op2)
			if (tipo1 != tipo2):
				print('Error de contexto.')
		elif(exp.tipo == 'ARITMETICA')
		elif(exp.tipo == 'BOOLEANA UNARIA'):

		elfi(exp.tipo == 'ARITMETICA UNARIA'):

		elif(exp.tipo == 'TERMINO'):



	def checkVar(self, var):
		# chequea que una variable exista en los scopes y devuelve su tipo
		# si no retorna, none
		for scope in self.scopes:
			if var in scope:
				return scope[var]
			else:
				print('Error de contexto. Variable no declarada.')
				sys.exit(0)


	def getTipoArreglo(self, arr):
		if (len(arr.hijos) > 0):
			for i in arr.hijos:
				tipo = self.getTipoArreglo(i)
				return tipo
		else:
			return arr.valor

	def nuevoScope(self, dec, tipo):
		# Scope actual
		top = self.scopes[0]

		if (dec.tipo == 'VARIABLE'):
			# Construimos objeto simbolo
			var = simbolo(dec.valor, tipo)
			# Agregamos simbolo a la tabla
			top[dec.valor] = var 

		
		# Recorremos arbol
		for i in dec.hijos:
			if (i.tipo == 'VARIABLE'):
				# Construir objeto simbolo
				var = simbolo(i.valor, tipo)
				# Agregamos simbolo a la tabla
				top[i.valor] = var 
				if (len(i.hijos)>0):
					for j in i.hijos:
						if (j.tipo == 'EXPRESION'):
							# Chequear que la expresion concuerde con el tipo
							# Guardarla en valor
							pass
						else:
							self.nuevoScope(j, tipo)

			else:
				tipo = i.valor
				for k in i.hijos:
					if (k.tipo == 'ARREGLO'):
						tipo = self.getTipoArreglo(k)
				self.nuevoScope(i, tipo)

class simbolo():
	def __init__(self, val, t):
		self.tipo = t
		self.valor = val





# Arreglar funcion de error del parser
# Extender el AST con informacion de los tipos
# Crear pila de scopes
# Un scope es un diccionario (tabla de hash)
# Recorrer AST y cada vez que encuentre una declaracion crear un scope nuevo
# Agregar variables de la declaracion al scope
	# Si se hace una asignacion en la declaracion: chequear que los tipos 
	# de la operacion sean correctos, si no error de contexto
# Agregar scope al top de la pila
# Para cualquier operacion dentro del bloque actual en el AST: chequear
# que los tipos sean correctos para las operaciones y que las varibles usadas
# esten en alguno de los scopes de la pila (que esten declaradas), si no error de contexto.
	# Chequear arreglos
	# Chequear asignaciones
	# Expresiones
	# Operaciones
# Una vez se llegue al final del bloque, remover el scope de la pila.


# DUDA: si se hace una asignacion dentro de un bloque a una variable declarada en un 
# bloque mas externo. Ese valor asignado queda guardado de forma global?


