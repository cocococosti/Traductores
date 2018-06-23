"""
Main del analizador sintactico para el lenguaje BasicTran

Autores:
Constanza Abarca
Pedro Maldonado

Fecha:
05/06/2018
"""
from parser import *

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