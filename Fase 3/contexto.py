import sys

class context:

	def __init__(self):
		# Inicializar pila de scopes (variables declaradas para cada bloque)
		self.scopes = []

	def contextCheck(self, ast):

		# Tomamos un arbol y recorremos sus hijos
		if (ast):
			if (len(ast.hijos) > 0): 

				for nodo in ast.hijos:

					if (nodo.tipo == 'BLOQUE'):

						for hijo in nodo.hijos:
							self.contextCheck(hijo)

						# Removemos el top de la pila
						self.scopes.pop(0)

					elif (nodo.tipo == 'DECLARACION'):
						# Creamos nuevo scope (por ahora vacio)
						scope = {}
						# Insertamos nuevo scope en la cabeza de la pila
						self.scopes.insert(0, scope)
						# Tipo de la declaracion
						tipo = nodo.valor
						# Para cada de una de las variables declaradas en el scope
						for k in nodo.hijos:
							# Si la variable es un arreglo entonces necesitamos hallar
							# el tipo de los elementos del arreglo
							if (k.tipo == 'ARREGLO'):
								tipo = self.getTipoArreglo(k)
						# Insertamos variables en el scope
						self.nuevoScope(nodo, tipo)

					elif (nodo.tipo == 'ASIGNACION'):
						# Si encontramos una operacion de tipo Asignacion, chequear que
						# la variable ha sido declarada y que el tipo concuerde
						var = self.checkVar(nodo.valor)
						tpe = self.checkExp(nodo.hijos[0])
						if (var.tipo != tpe):
							print("Error de contexto. Tipo incorrectos.")
							sys.exit(0)

					elif (nodo.tipo == 'EXPRESION'):
						self.checkExp(nodo)
						
					else:
						self.contextCheck(nodo)

	def getTipoArreglo(self, arr):
		# Recorremos los hijos del arreglo
		# (pues puede ser un arreglo de arreglos)
		if (len(arr.hijos) > 0):
			for i in arr.hijos:
				tipo = self.getTipoArreglo(i)
				return tipo
		# Cuando el arreglo no tenga mas hijos, en valor estara guardado el tipo
		else:
			return arr.valor

	def nuevoScope(self, dec, tipo):
		# Scope actual
		top = self.scopes[0]

		# En una declaracion podemos estar declarando variable solas
		# o arreglos
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

	def checkExp(self, exp):
		# Chequea si las operaciones de la expr son correctas
		# y retorna el tipo resultante 
		# Usarla de forma recursiva con cada subexpresion
		# retorna error si se obtiene tipos distintos

		for hijo in exp.hijos:
			if (hijo.tipo == 'BOOLEANA'):
				op1 = hijo.hijos[0]
				op2 = hijo.hijos[1]
				tipo1 = self.checkExp(op1)
				tipo2 = self.checkExp(op2)
				if (tipo1 != tipo2):
					print('Error de contexto. Tipo incorrecto booleana.')
					sys.exit(0)

			elif (hijo.tipo == 'RELACIONAL'):

				op1 = hijo.hijos[0]
				op2 = hijo.hijos[1]

				tipo1 = self.checkExp(op1)
				tipo2 = self.checkExp(op2)
				if (tipo1 != tipo2):
					print('Error de contexto. Tipo incorrecto relacional.')
					sys.exit(0)
				else:
					return "bool"

			elif(hijo.tipo == 'BIN_ARITMETICA'):
				op1 = hijo.hijos[0]
				op2 = hijo.hijos[1]
				tipo1 = self.checkExp(op1)
				tipo2 = self.checkExp(op2)
				if (tipo1 != tipo2):
					print('Error de contexto. Tipo incorrecto aritmetica.')
					sys.exit(0)
				else:
					return tipo1
			elif(hijo.tipo == 'BOOLEANA UNARIA'):
				pass

			elif(hijo.tipo == 'ARITMETICA UNARIA'):
				pass

			elif(hijo.tipo == 'TERMINO'):
				return hijo.type



	def checkVar(self, var):
		# chequea que una variable exista en los scopes y devuelve su tipo
		# si no retorna, none
		for i in range(len(self.scopes)):
			if var in self.scopes[i]:
				return self.scopes[i][var]
			else:
				print('Error de contexto. Variable no declarada.')
				sys.exit(0)





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


