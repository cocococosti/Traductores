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

def p_programa(p):
	'''
	expresion : TkBegin expresion TkEnd
	'''
	p[0] = (p[1], p[2], p[3])



def p_condicional(p):
	'''
	expresion : TkIf condicion TkHacer cuerpo TkEnd
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_cuerpo(p):
	'''
	cuerpo : expresion cuerpo
		   | expresion
	'''
	p[0] = p[1]
	print(p[0])

def p_expresion(p):
	'''
	expresion : expresion TkResta expresion
			  | expresion TkSuma expresion
			  | expresion TkDiv expresion
			  | expresion TkMult expresion
			  | expresion TkMod expresion
	'''
	p[0] = (p[1], p[2], p[3])

def p_guardia(p):
	'''
	condicion : expresion TkMenor expresion
			  | expresion TkMayor expresion
	'''

	p[0] = (p[2], p[1], p[3])


def p_terminal(p):
	'''
	expresion : TkNum
			  | TkId
	'''
	p[0] = p[1]

def p_error(p):
	print("Syntax error in input!")

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
print(p)

