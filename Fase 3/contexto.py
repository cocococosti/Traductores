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
						self.contextCheck(nodo)

						# Removemos el top de la pila al terminar con este bloque
						self.scopes.pop(0)

					elif (nodo.tipo == 'DECLARACION'):
						# Creamos nuevo scope (por ahora vacio)
						scope = {}
						# Insertamos nuevo scope en la cabeza de la pila
						self.scopes.insert(0, scope)
						self.nuevoScope(nodo)


					elif (nodo.tipo == 'ASIGNACION'):
						# Si encontramos una operacion de tipo Asignacion, chequear que
						# la variable ha sido declarada y que el tipo concuerde

						#Obtengamos id
						if (isinstance(nodo.valor, str)):
							var = self.checkVar(nodo.valor)
							if (var.contador):
								print("se trata de modificar la variable que pertenece a una iteracion.")
								sys.exit(0)
							var = var.tipo
						else:
							var = self.getTipoId(nodo.valor)

						# Si la var es de un arreglo chequear que el indice es de tipo entero
						tpe = self.checkExp(nodo.hijos[0])

						if (var != tpe):
							print("Error de contexto. Tipo incorrectos.")
							sys.exit(0)

					
					elif(nodo.tipo == 'CONDICIONAL'):

						for h in nodo.hijos:

							# Recorrer el cuerpo de forma recursiva
							if (h.tipo == 'CUERPO'):
								self.contextCheck(h)
							# Chequear que la condicion sea de tipo booleana
							else:
								t = self.checkExp(h)

								if (t != 'bool'):
									print("Error de contexto. Tipo incorrectos.")
									sys.exit(0)

					elif (nodo.tipo == 'ITERACION INDETERMINADA'):
						hijo = nodo.valor
						op1 = hijo.hijos[0]
						op2 = hijo.hijos[1]

						tipo1 = self.checkExp(op1)
						tipo2 = self.checkExp(op2)

						if (hijo.valor != '/=' and hijo.valor != '='):
							if (tipo1 != 'int' or tipo2 != 'int'):
								print('Error de contexto. Tipo incorrecto relacional.')
								sys.exit(0)


						if (tipo1 != tipo2):
							print('Error de contexto. Tipo incorrecto relacional.')
							sys.exit(0)
						else:
							t = 'bool'
						
						if (t != 'bool'):
							print("Error de contexto. Tipo incorrectos.")
							sys.exit(0)
						
						self.contextCheck(nodo.hijos[0])

					elif (nodo.tipo == 'ITERACION DETERMINADA'):

						# agregar atributo a la var de iteracion, set to true 
						# al salir de los hijos del ciclo set to false

						cont = nodo.valor[0]
						scope = {}
						scope[cont] = simbolo(cont, 'int')
						scope[cont].contador = True

						# Chequear que los rangos sean enteros
						limInf = nodo.valor[1]
						tipoInf = self.checkExp(limInf)
						limSup = nodo.valor[2]
						tipoSup = self.checkExp(limSup)

						if (tipoSup != tipoInf != 'int'):
							print('Error de contexto. Rangos del ciclo no son enteros.')
							sys.exit(0)

						step = nodo.valor[3]

						if (step != '1'):
							if (step.tipo == 'TERMINO'):
								if (len(step.hijos)>0):
									t = self.checkExp(step)
								else:
									t = step.type
							else:
								t = self.checkExp(step)

							if (t != 'int'):
								print('Error de contexto.')
								sys.exit(0)




						# Insertamos nuevo scope en la cabeza de la pila
						self.scopes.insert(0, scope)



						self.contextCheck(nodo.hijos[0])
						
						# set aqui
						self.scopes.pop(0)
					else:
						self.contextCheck(nodo)

	def checkTipoArrOfArr(self,arr):
		# Cheuqear tipo del indice
		t = self.getTipoId(arr.arreglo)
		if (t != 'int'):
			print('Error de contexto. Tipo incorrecto para indice del arreglo.')
			sys.exit(0)
		if (len(arr.hijos)>0):
			for i in arr.hijos:
				self.checkTipoArrOfArr(i)

		#chequear var del arreglo

		#chequear indice del arreglo


	def getTipoId(self, indice):
		# Chequea tipo del indice y lo retorna si es correcto
		# var -> nombre de la variable que contiene el arreglo
		# indice -> indice a acceder del arreglo


		# Obtengamos tipo del indice
		if (indice.tipo == 'BIN_ARITMETICA'):
			tipoIndex = self.checkExp(indice)
		elif (indice.tipo == 'TERMINO'):
			if (len(indice.hijos) > 0):
				for hijo in indice.hijos:
					tipoIndex = self.getTipoId(hijo)
					if (tipoIndex != 'int'):
						print('Error de contexto. Tipo incorrecto para indice del arreglo.')
						sys.exit(0)
			else:
				return indice.type
		elif (indice.tipo == 'VAR_ARREGLO'):
			t = self.checkVar(indice.valor)
			for hijo in indice.hijos:
				tipoIndex = self.getTipoId(hijo)

			if (t.tipo != tipoIndex != 'int'):
				print('Error de contexto. Tipo incorrecto para indice del arreglo.')
				sys.exit(0)

			return t.tipo



	def getTipo(self, arr):
		# Recorremos los hijos del arreglo
		# (pues puede ser un arreglo de arreglos)
		if (len(arr.hijos) > 0):
			for i in arr.hijos:
				tipo = self.getTipo(i)
				return tipo
		# Cuando el arreglo no tenga mas hijos, en valor estara guardado el tipo
		else:
			return arr.valor

	def nuevoScope(self, dec):

		# Tipo de la declaracion
		tipo = dec.valor

		# Los hijos de una variable pueden ser un conjunto de variables, un arreglo
		# u otra declaracion
		for k in dec.hijos:

			if (k.tipo == 'ARREGLO'):
				# Si la variable es un arreglo entonces necesitamos hallar
				# el tipo de los elementos del arreglo
				tipo = self.getTipo(k)
				# Si es un arreglo tambien hay que chequear el tamaño
				# sea de tipo entero
				self.checkTipoArrOfArr(k)

			elif (k.tipo == 'DECLARACION'):
				self.nuevoScope(k)

			elif (k.tipo == 'VARIABLE'):
				self.agregarSimbolo(k, tipo)
				

		
	def agregarSimbolo(self, var, tipo):
		
		# scope actual
		top = self.scopes[0]
		# Construimos objeto simbolo
		variable = simbolo(var.valor, tipo)
		# Agregamos simbolo a la tabla
		top[var.valor] = variable

		# Recorremos arbol
		if ((len(var.hijos))>0):
			for i in var.hijos:
				if (i.tipo == 'VARIABLE'):
					self.agregarSimbolo(i, tipo)
				elif (i.tipo == 'EXPRESION'):
					t = checkExp(i)
					if (t != tipo):
						print('Error de contexto. Tipo incorrecto.')
						sys.exit(0)
					else:
						top[var.valor].asignado = i


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
				if (tipo1 != tipo2 != 'bool'):
					print('Error de contexto. Tipo incorrecto booleana.')
					sys.exit(0)
				else:
					return 'bool'

			elif (hijo.tipo == 'RELACIONAL'):

				op1 = hijo.hijos[0]
				op2 = hijo.hijos[1]

				tipo1 = self.checkExp(op1)
				tipo2 = self.checkExp(op2)

				if (hijo.valor != '/=' and hijo.valor != '='):
					if (tipo1 != 'int' or tipo2 != 'int'):
						print('Error de contexto. Tipo incorrecto relacional.')
						sys.exit(0)


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
				if (tipo1 != tipo2 != 'int'):
					print('Error de contexto. Tipo incorrecto aritmetica.')
					sys.exit(0)
				else:
					return 'int'
			elif(hijo.tipo == 'BOOLEANA UNARIA'):
				op = hijo.hijos[0]
				tipo = self.checkExp(op)
				if (tipo != 'bool'):                    
					print('Error de contexto. Tipo incorrecto booleana unaria.')
				else:
					return "bool"

			elif(hijo.tipo == 'OPERACION UNARIA'):
				op = hijo.hijos[0]
				tipo = self.checkExp(op)
				if (tipo != 'int'):
					print('Error de contexto. Tipo incorrecto aritmetica unaria.')

			elif(hijo.tipo == "OPERACION CARACTER"):
			
				t = self.checkExp(hijo)
				if (t != 'char'):
					print('Error de contexto. Tipo incorrecto caracter.')
					sys.exit(0)
				else:
					return 'char'
			elif(hijo.tipo == 'TERMINO'):
				if (hijo.type == 'var'):
					
					t = self.checkVar(hijo.lexeme)

					return t.tipo
				else:
					return hijo.type
			
			elif(hijo.tipo == 'VAR_ARREGLO'):
				# Chequear que indices son correctos
				index = self.getTipoId(hijo.hijos[0])
				if (index != 'int'):
					print('Error de contexto. Tipo incorrecto indice.')
					sys.exit(0)
				#retorna tipo del arreglo
				t = self.checkVar(hijo.valor)

				return t.tipo




	def checkVar(self, var):
		# chequea que una variable exista en los scopes y devuelve su tipo
		# si no retorna, none

		# chequeeemos que la variable no esta siendo redeclarada
		top = self.scopes[0]

		if var in top:
			print('Error. Variable ya declarada.')
			sys.exit(0)

		for i in range(len(self.scopes)):
			if var in self.scopes[i]:
				return self.scopes[i][var]
		
		print('Error de contexto. Variable ' + var + ' no declarada.')
		sys.exit(0)





class simbolo():
	def __init__(self, val, t):
		self.tipo = t # tipo de la variable
		self.valor = val # identificador o valor de la variable
		self.asignado = None # valor del simbolo en caso de que se trate de una var
		self.contador = None # para chequear si una variable esta siendo usada como contador





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


