"""
Implementación de un analizador sintactico para el lenguaje BasicTran

Autores:
Constanza Abarca
Pedro Maldonado

Fecha:
05/06/2018
"""

import ply.yacc as yacc
from Lex import tokens
from sys import argv
import sys
from arbol import *

# Lista de precedencias 
precedence = (
	('nonassoc', 'TkMayor', 'TkMenor', 'TkMayorIgual', 'TkMenorIgual'),
	('left', 'TkSuma', 'TkResta'),
	('left', 'TkMult', 'TkDiv', 'TkMod'),
	('right', 'uminus'),
	('left', 'TkConcatenacion'),
	('left', 'TkShift'),
	('left', 'TkCorcheteAbre', 'TkCorcheteCierra'),
	('left', 'TkPunto'),
	('left', 'TkSiguienteCar'),
	('left', 'TkAnteriorCar'),
	('left', 'TkValorAscii'),
	('left', 'TkIgual', 'TkDesigual'),
	('left', 'TkConjuncion', 'TkDisyuncion'),
	('right', 'TkNot')
)

# Regla principal, define un bloque de instrucciones
def p_programa(p):
	'''
	bloque : TkBegin cuerpo TkEnd
		   | TkWith declaracion TkBegin cuerpo TkEnd
	'''
	if (len(p) == 4):
		p[0] = Nodo('BLOQUE', None, [p[2]])
		#p[0] = (p[2])
	else:
		p[0] = Nodo('BLOQUE', None, [p[2], p[4]])
		#p[0] = (p[4])


# Regla para declaraciones de variables y su tipo
def p_declaracion(p):
	'''
	declaracion : TkVar variables TkDosPuntos TkInt
			    | TkVar variables TkDosPuntos TkBool
			    | TkVar variables TkDosPuntos TkChar
			    | TkVar variables TkDosPuntos arreglo
			    | TkVar variables TkDosPuntos TkInt variables
			    | TkVar variables TkDosPuntos TkBool variables
			    | TkVar variables TkDosPuntos TkChar variables
			    | TkVar variables TkDosPuntos arreglo variables

	'''
	p[0] = Nodo('DECLARACION', None, [p[2]])

# Definicion de arreglos
def p_arreglo(p):
	'''
	arreglo : TkArray TkCorcheteAbre TkNum TkCorcheteCierra TkOf TkChar
		    | TkArray TkCorcheteAbre TkNum TkCorcheteCierra TkOf TkInt
		    | TkArray TkCorcheteAbre TkNum TkCorcheteCierra TkOf TkBool
		    | TkArray TkCorcheteAbre TkNum TkCorcheteCierra TkOf arreglo
		    | TkArray TkCorcheteAbre TkId TkCorcheteCierra TkOf TkChar
		    | TkArray TkCorcheteAbre TkId TkCorcheteCierra TkOf TkInt
		    | TkArray TkCorcheteAbre TkId TkCorcheteCierra TkOf TkBool
		    | TkArray TkCorcheteAbre TkId TkCorcheteCierra TkOf arreglo
		    | TkArray TkCorcheteAbre opAritm TkCorcheteCierra TkOf TkChar
		    | TkArray TkCorcheteAbre opAritm TkCorcheteCierra TkOf TkInt
		    | TkArray TkCorcheteAbre opAritm TkCorcheteCierra TkOf TkBool
		    | TkArray TkCorcheteAbre opAritm TkCorcheteCierra TkOf arreglo
	'''
	p[0] = Nodo('ARREGLO', None, None)

# Regla de valores terminales
def p_terminal(p):
	'''
	terminal : TkId
			  | TkCaracter
			  | TkNum
			  | TkTrue
			  | TkFalse
			  | TkTab
			  | TkSalto
			  | TkComilla
			  | TkBarra
			  | TkId TkCorcheteAbre TkNum TkCorcheteCierra
			  | TkParAbre terminal TkParCierra
	'''
	if (len(p) == 5):
		p[0] = Nodo("TERMINO", p[1]+p[2]+str(p[3])+p[4], None)
	else:
		p[0] = Nodo('TERMINO', p[1], None)

# Regla para definir el cuerpo de un bloque (conjunto de instrucciones)
def p_cuerpo(p):
	'''
	cuerpo : instruccion
		   | instruccion cuerpo
		   | bloque cuerpo
		   | bloque
	'''
	p[0] = Nodo("CUERPO", None, [p[1]])
	if (len(p) == 2):
		p[0] = Nodo("CUERPO", None, [p[1]])
		#p[0] = (p[1])
	else:
		p[0] = Nodo("CUERPO", None, [p[1], p[2]])


# Definicion de una instruccion
def p_instruccion(p):
	'''
	instruccion : expresion TkPuntoYComa
				| condicional
				| iterDeter
				| iterInd
				| asignacion TkPuntoYComa
				| input TkPuntoYComa
				| output TkPuntoYComa

	'''
	
	p[0] = Nodo("INSTRUCCION", None, [p[1]])


# Definicion de instrucciones condicionales
def p_condicional(p):
	'''
	condicional : TkIf opBool TkHacer cuerpo TkEnd
			    | TkIf opBool TkHacer cuerpo TkOtherwise TkHacer cuerpo TkEnd
			    | TkIf opRel TkHacer cuerpo TkEnd
			    | TkIf opRel TkHacer cuerpo TkOtherwise TkHacer cuerpo TkEnd
			    | TkIf terminal TkHacer cuerpo TkEnd
			    | TkIf terminal TkHacer cuerpo TkOtherwise TkHacer cuerpo TkEnd


	'''
	if (len(p) == 8):
		p[0] = Nodo("CONDICIONAL", None, [p[2], p[4], p[6]])
	else:
		p[0] = Nodo("CONDICIONAL", None, [p[2], p[4]])

# Definicion de asignaciones
def p_asignacion(p):
	'''
	asignacion : TkId TkAsignacion expresion
	'''
	p[0] = Nodo("ASIGNACION", p[1], [p[3]])

# Entrada
def p_input(p):
	'''
	input : TkRead TkId
	'''
	p[0] = Nodo("ENTRADA", p[1], [p[2]])

#Salida
def p_output(p):
	'''
	output : TkPrint expresion
	'''
	p[0] = Nodo("SALIDA", p[1], [p[2]])

# Cliclos while
def p_iteracionind(p):
    '''
    
    iterInd : TkWhile opRel TkHacer cuerpo TkEnd
            | TkWhile opBool TkHacer cuerpo TkEnd
    '''
    
    p[0] = Nodo("ITERACION INDETERMINADA", p[2], [p[4]])

# Ciclos for
def p_iterDeter(p):
	'''
	iterDeter : TkFor TkId TkFrom opAritm TkTo opAritm TkStep opAritm TkHacer cuerpo TkEnd
			  | TkFor TkId TkFrom opAritm TkTo terminal TkStep opAritm TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo opAritm TkStep opAritm TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo terminal TkStep opAritm TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom opAritm TkTo opAritm TkStep terminal TkHacer cuerpo TkEnd
			  | TkFor TkId TkFrom opAritm TkTo terminal TkStep terminal TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo opAritm TkStep terminal TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo terminal TkStep terminal TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom opAritm TkTo opAritm TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom opAritm TkTo terminal TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo opAritm TkHacer cuerpo TkEnd
	          | TkFor TkId TkFrom terminal TkTo terminal TkHacer cuerpo TkEnd
	'''
	if (len(p) == 12):
		p[0] = Nodo("ITERACION DETERMINADA", [p[2], p[4], p[6], p[8]], [p[10]])
	else:
		p[0] = Nodo("ITERACION DETERMINADA", [p[2], p[4], p[6], "1"], [p[8]])

# Exoresiones generales
def p_expresion(p):
	'''
	expresion : opAritm
              | terminal
              | opRel
              | opCar
              | opBool
	'''
	p[0] = Nodo("EXPRESION", None, [p[1]])

def p_opAritm(p):
	'''
	opAritm : expresion TkResta expresion
		    | expresion TkSuma expresion
		    | expresion TkDiv expresion
	        | expresion TkMult expresion
	        | expresion TkMod expresion
	        | expresion TkConcatenacion expresion
	        | expresion TkPunto expresion
			| TkParAbre expresion TkResta expresion TkParCierra
		    | TkParAbre expresion TkSuma expresion TkParCierra
		    | TkParAbre expresion TkDiv expresion TkParCierra
	        | TkParAbre expresion TkMult expresion TkParCierra
	        | TkParAbre expresion TkMod expresion TkParCierra
	        | TkParAbre expresion TkConcatenacion expresion TkParCierra
	        | TkParAbre expresion TkPunto expresion TkParCierra
	        | TkResta expresion %prec uminus
	        | TkParAbre TkResta expresion TkParCierra %prec uminus
	        | TkShift expresion
	        | TkParAbre TkShift expresion TkParCierra

	'''
	if (len(p) == 6):
		p[0] = Nodo("BIN_ARITMETICA", p[3], [p[2], p[4]])
	elif (len(p) == 3):
		p[0] = Nodo("OPERACION UNARIA", p[1], [p[2]])
	elif (len(p) == 5):
		p[0] = Nodo("OPERACION UNARIA", p[2], [p[3]])
	else:
		p[0] = Nodo("BIN_ARITMETICA", p[2], [p[1], p[3]])
	#p[0] = (p[1], p[2], p[3])

def p_opCar(p):
	'''
	opCar : terminal TkSiguienteCar
		  | terminal TkAnteriorCar
	      | TkValorAscii terminal
	      | TkValorAscii terminal TkSiguienteCar
	      | TkValorAscii terminal TkAnteriorCar

	'''
	if (p[1] == '#'):
		if (len(p) == 3):
			p[0] = Nodo("OPERACION CARACTER", p[1], [p[2]])
		else:
			p[0] = Nodo("OPERACION CARACTER", p[1], [Nodo("OPERACION CARACTER", p[3], [p[2]])])
	else:
		p[0] = Nodo("OPERACION CARACTER", p[2], [p[1]])


def p_opRel(p):
	'''
	opRel : expresion TkMayor expresion
		  | expresion TkMenor expresion
		  | expresion TkMayorIgual expresion
		  | expresion TkMenorIgual expresion
		  | expresion TkIgual expresion
		  | expresion TkDesigual expresion
		  | TkParAbre expresion TkMayor expresion TkParCierra
		  | TkParAbre expresion TkMenor expresion TkParCierra
		  | TkParAbre expresion TkMayorIgual expresion TkParCierra
		  | TkParAbre expresion TkMenorIgual expresion TkParCierra
		  | TkParAbre expresion TkIgual expresion TkParCierra
		  | TkParAbre expresion TkDesigual expresion TkParCierra
	'''
	if (len(p) == 6):
		p[0] = Nodo("RELACIONAL", p[3], [p[2], p[4]])
	else:
		p[0] = Nodo("RELACIONAL", p[2], [p[1], p[3]])

# Definicion de las variables que corresponden a una declaracion
def p_variables(p):
	'''
	variables : TkId TkComa variables
			  | TkId TkAsignacion expresion TkComa variables
			  | TkId 
			  | TkId TkAsignacion expresion
	'''
	if (len(p) == 4):
		p[0] = Nodo('VARIABLE', p[1], [p[3]])
	elif (len(p) == 6):
		p[0] = Nodo('VARIABLE', p[1], [p[3], p[5]])
	else:
		p[0] = Nodo('VARIABLE', p[1], None)

# Definicion de operaciones booleanas
def p_opBool(p):
	'''
	opBool : expresion TkConjuncion expresion
           | expresion TkDisyuncion expresion
           | TkParAbre expresion TkConjuncion expresion TkParCierra
           | TkParAbre expresion TkDisyuncion expresion TkParCierra
           | TkNot expresion
           | TkParAbre TkNot expresion TkParCierra

	'''
	if (len(p) == 4):
		p[0] = Nodo("BOOLEANA", p[2], [p[1], p[3]])
	elif (len(p) == 3):
		p[0] = Nodo("BOOLEANA UNARIA", p[1], [p[2]])
	elif (len(p) == 5):
		p[0] = Nodo("BOOLENA UNARIA", p[2], [p[3]])
	elif(len(p) == 2):
		p[0] = Nodo("TERMINO", p[1], [])
	else:
		p[0] = Nodo("BOOLEANA", p[3], [p[2], p[4]])

# Regla para errores
def p_error(p):
	print("\nError de sintaxis")
	sys.exit(0)

# Imprimir las expresiones aritmeticas
def imprimirAritm(nodo, tabs):
	# Tipo de expresion
	print(tabs + nodo.tipo)
	# Tipo de operacion
	print(tabs + "- Operacion: " + nodo.valor)

	# Si hay un nodo (disitinto de None)
	if (nodo):
		# Si el nodo tiene hijos 
		if (len(nodo.hijos) > 0):
			# Los hijos son los operadores de la expresion
			izq = nodo.hijos[0]
			der = nodo.hijos[1]

			# Operador izquierdo
			print(tabs + "- Operador izquierdo: ")
			if (izq.tipo == "EXPRESION"):
				imprimirExp(izq, tabs + "\t")
			elif (izq.tipo == "TERMINO"):
				print(tabs + "\t" + izq.tipo)
				print(tabs + "\t" + "Valor: " + str(izq.valor))

			# Operador derecho
			print(tabs + "- Operador derecho: ")
			if (der.tipo == "EXPRESION"):
				imprimirExp(der, tabs + "\t")
			elif (der.tipo == "TERMINO"):
				print(tabs + "\t" + der.tipo)
				print(tabs + "\t" + "- Valor: " + str(der.valor))

# Funcion general para imprimir cualquier expresion
def imprimirExp(nodo, tabs):
	hijo = nodo.hijos[0]
	# Los hijos del nodo son cualquier tipo de expresion
	if (hijo.tipo == "BIN_ARITMETICA"):
		imprimirAritm(hijo, tabs)
	elif (hijo.tipo == "EXPRESION"):
		imprimirExp(hijo, tabs)
	elif (hijo.tipo == "TERMINO"):
		print(tabs + hijo.tipo)
		print(tabs + "- Valor: " + str(hijo.valor))
	elif (hijo.tipo == "OPERACION UNARIA"):
		imprimirUnaria(hijo, tabs)
	elif (hijo.tipo == "RELACIONAL"):
		imprimirRelacional(hijo, tabs)
	elif (hijo.tipo == "OPERACION CARACTER"):
		imprimirCaracter(hijo, tabs)
	elif (hijo.tipo == "BOOLEANA" or hijo.tipo == "BOOLEANA UNARIA"):
		imprimirBool(hijo, tabs)

# Para imprimir exp booleanas
def imprimirBool(nodo, tabs):

	print(tabs + nodo.tipo)

	if (len(nodo.hijos) > 0):
		print(tabs + "- Operacion: " + nodo.valor)
		if (len(nodo.hijos) == 2):
			# Sus hijos son los operadores
			print(tabs + "- Operador izquierdo: ")
			imprimirExp(nodo.hijos[0], tabs+"\t")
			print(tabs + "- Operador derecho: ")
			imprimirExp(nodo.hijos[1], tabs+"\t")
		else:
			print(tabs + "- Operador: ")
			imprimirExp(nodo.hijos[0], tabs+"\t")
	else:
		print(tabs + "- Valor:")
		print(tabs+"\t" + nodo.valor)

# Para imprimir declaracion de variables
def imprimirDeclaracion(nodo, tabs):
	if (nodo):
		if (len(nodo.hijos) > 0):
			for i in nodo.hijos:
				if (i.tipo == "VARIABLE"):
					print(tabs + i.tipo)
					print(tabs + "- Identificador: " + i.valor)
					for j in i.hijos:
						if (j.tipo == "EXPRESION"):
							print(tabs + "- Valor: ")
							imprimirExp(j, tabs+"\t")
						else:
							print(tabs + "- Valor: no asignado")
					
				imprimirDeclaracion(i, tabs)

# Para imprimir expresiones con caracteres
def imprimirCaracter(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Operacion: " + nodo.valor)

	hijo = nodo.hijos[0]

	if (hijo.tipo == "OPERACION CARACTER"):
		print(tabs + "- Operador")
		imprimirCaracter(hijo, tabs+"\t")
	elif (hijo.tipo == "TERMINO"):
		print(tabs + "- Operador")
		print(tabs + "\t" + hijo.tipo)
		print(tabs + "\t" + str(hijo.valor))

# Para imprimir expresiones relacionales
def imprimirRelacional(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Operacion: " + nodo.valor)

	if (nodo):
		if (len(nodo.hijos) > 0):
			izq = nodo.hijos[0]
			der = nodo.hijos[1]

			if (izq.tipo == "EXPRESION"):
				print(tabs + "- Operador izquierdo: ")
				imprimirExp(izq, tabs + "\t")
			elif (izq.tipo == "TERMINO"):
				print(tabs + "- Operador izquierdo: ")
				print(tabs + "\t" + izq.tipo)
				print(tabs + "\t" + "Valor: " + str(izq.valor))

			if (der.tipo == "EXPRESION"):
				imprimirExp(der, tabs + "\t")
			elif (der.tipo == "TERMINO"):
				print(tabs + "- Operador derecho: ")
				print(tabs + "\t" + der.tipo)
				print(tabs + "\t" + "Valor: " + str(der.valor))

# Para imprimir ciclos for
def imprimirIterDeter(nodo, tabs):
	print(tabs + nodo.tipo)
	inf = nodo.valor[1]
	sup = nodo.valor[2]
	step = nodo.valor[3]
	print(tabs + "- Identificador: " + nodo.valor[0])
	print(tabs + "- Limite inferior: ")
	if (inf.tipo == "TERMINO"):
		print(tabs + "\t" + inf.tipo)
		print(tabs + "\t" + str(inf.valor))
	elif (inf.tipo == "BIN_ARITMETICA"):
		imprimirAritm(inf, tabs + "\t")
	print(tabs + "- Limite superior: ")
	if (sup.tipo == "TERMINO"):
		print(tabs + "\t" + sup.tipo)
		print(tabs + "\t" + str(sup.valor))
	elif (sup.tipo == "BIN_ARITMETICA"):
		imprimirAritm(sup, tabs + "\t")
	print(tabs + "- Step: ")
	if (step == "1"):
		print(tabs + "\t" + "TERMINO")
		print(tabs + "\t" + step)
	else:	
		if (step.tipo == "TERMINO"):
			print(tabs + "\t" + step.tipo)
			print(tabs + "\t" + str(step.valor))
		elif (step.tipo == "BIN_ARITMETICA"):
			imprimirAritm(step, tabs + "\t")
	print(tabs + "- Operaciones")
	imprimirArbol(nodo.hijos[0], tabs + "\t")

# Para imprimir expresiones unarias
def imprimirUnaria(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "Operacion: " + nodo.valor)
	print(tabs + "Operador: ")
	if (nodo.hijos[0].tipo == "TERMINO"):
		print(tabs + "\t" + "TERMINO")
		print(tabs + "\t" + str(nodo.hijos[0].valor))
	elif (nodo.hijos[0].tipo == "OPERACION UNARIA"):
		imprimirUnaria(nodo.hijos[0], tabs + "\t")
	elif (nodo.hijos[0].tipo == "EXPRESION"):
		imprimirExp(nodo.hijos[0], tabs + "\t")
	else:
		imprimirAritm(nodo.hijos[0], tabs + "\t")

# Para asignaciones
def imprimirAsig(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "Identificador: " + nodo.valor)
	print(tabs + "Valor: ")

	imprimirExp(nodo.hijos[0], tabs + "\t")

# Para condicionales
def imprimirCond(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Guardia")
	imprimirBool(nodo.hijos[0], tabs + "\t")
	if (len(nodo.hijos) == 3):
		print(tabs + "- Exito")
		imprimirArbol(nodo.hijos[1], tabs + "\t")
		print(tabs + "- Otherwise")
		imprimirArbol(nodo.hijos[2], tabs + "\t")
	else:
		print(tabs + "- Exito")
		imprimirArbol(nodo.hijos[1], tabs + "\t")

# Para entradas
def imprimirEntrada(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Operador: " + nodo.valor)
	print(tabs + "-Identificador: " + nodo.hijos[0])

# Para salidas
def imprimirSalida(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Operador: " + nodo.valor)
	print(tabs + "-Salida: ")
	imprimirExp(nodo.hijos[0], tabs + "\t")

# Para imprimir while loop
def imprimirIndeter(nodo, tabs):
	print(tabs + nodo.tipo)
	print(tabs + "- Guardia: ")
	if (nodo.valor.tipo == "RELACIONAL"):
		imprimirRelacional(nodo.valor, tabs + "\t")
	else:
		imprimirBool(nodo.valor, tabs + "\t")
	print(tabs + "- Exito: ")
	imprimirArbol(nodo.hijos[0], tabs + "\t")

# Para imprimir todo el arbol de expresiones
def imprimirArbol(nodo, tabs):
	if (nodo):
		if (len(nodo.hijos) > 0):
			for i in nodo.hijos:
				if (i.tipo == "BLOQUE"):
					tabs = tabs + "\t"
					print("\n")
					print(tabs + i.tipo)
				
				if (i.tipo == "EXPRESION"):
					print("\n")
					imprimirExp(i, tabs)

				elif (i.tipo == "DECLARACION"):
					print("\n")
					print(tabs + i.tipo)
					imprimirDeclaracion(i, tabs)

				elif(i.tipo == "ITERACION DETERMINADA"):
					print("\n")
					imprimirIterDeter(i, tabs)

				elif (i.tipo == "ITERACION INDETERMINADA"):
					print("\n")
					imprimirIndeter(i, tabs)					

				elif (i.tipo == "ASIGNACION"):
					print("\n")
					imprimirAsig(i, tabs)

				elif (i.tipo == "CONDICIONAL"):
					print("\n")
					imprimirCond(i, tabs)
				elif (i.tipo == "SALIDA"):
					print("\n")
					imprimirSalida(i, tabs)
				elif (i.tipo == "ENTRADA"):
					print("\n")
					imprimirEntrada(i, tabs)
				else:
					imprimirArbol(i, tabs)
				

def main():
	# Leer nombre del archivo de la entrada estandar
	filename = argv[1]

	# String con todas las lineas del archivo
	program = ""

	# Numero total de lienas en el archivo
	n = 0
	parser = yacc.yacc()

	with open(filename, 'r') as fd:

		for line in fd:
			program = program + line
			n = n + 1

	p = parser.parse(program)

	print("SECUENCIACION")
	s = "\t"

	imprimirArbol(p, s)

main()